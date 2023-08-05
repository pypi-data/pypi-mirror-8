"""Process messages off the queue, including mapping, combining, and reducing.
"""

import sys
import logging
import functools
import types
import traceback
import json
import time
import pprint
import itertools
import collections

import gevent.pool

import etcd.exceptions

import mr.config
import mr.config.queue
import mr.config.result
import mr.models.kv.job
import mr.models.kv.step
import mr.models.kv.handler
import mr.models.kv.invocation
import mr.models.kv.trees.relationships
import mr.models.kv.trees.sessions
import mr.models.kv.queues.dataset
import mr.models.kv.data_layer
import mr.models.kv.request
import mr.queue.queue_manager
import mr.workflow_manager
import mr.shared_types
import mr.constants
import mr.handlers.scope
import mr.utility

_logger = logging.getLogger(__name__)
_flow_logger = _logger.getChild('flow')

# TODO(dustin): We can maintain a nice little cache if the whole cluster pushes 
#               updates to it.

# TODO(dustin): We still have to deal with KV changes not yet having propagated 
#               by the time a queued message is picked-up by a worker.

# TODO(dustin): We might push changes into both *etcd* and *memcache*. Since 
#               there might be only one instance of memcache (and entirely in 
#               memory) vs many instances of *etcd* (and entirely on disk), it 
#               might provide us immediate concurrency while not completely 
#               sacrificing durability (if the process going down, there should 
#               still be a high degree of synchronization).

HANDLER_CTX_CLS = collections.namedtuple('HANDLER_CTX_CLS', 
                                         ('session_get', 'session_set', 
                                          'session_list'))

#_request_logger = logging.getLogger('request-log')
#
#def _get_mr_log(request, path_type, message, severity='info'):
#    l = _request_logger.getChild(request.request_id).getChild(path_type)
#    getattr(l, severity)(message)

class _QueuePusher(object):
    def __init__(self):
        self.__q = mr.queue.queue_manager.get_queue()

    def queue_map_step_from_parameters(self, message_parameters):
# TODO(dustin): We might increment a count of total steps processed on the 
#               request.

        if message_parameters.handler.required_capability != \
                mr.constants.REQUIRED_CAP_NONE:
            capability_name = message_parameters.handler.required_capability
        else:
            capability_name = mr.constants.CAP_GENERAL

        replacements = {
            'workflow_name': message_parameters.workflow.workflow_name,
            'capability_name': capability_name,
        }

        topic = mr.config.queue.TOPIC_NAME_MAP_TEMPLATE % replacements

        self.__q.producer.push_one(
            topic, 
            mr.constants.D_MAP, 
            message_parameters)

    def queue_initial_map_step_from_parameters(self, message_parameters):
        return self.queue_map_step_from_parameters(message_parameters)

    def queue_reduce_step_from_parameters(self, message_parameters, 
                                          parent_invocation):
        """We're reflecting (switch directions from mapping to reduction). The 
        current step is an action step (no mappings were done). The next 
        invocation will successively take the invocation-IDs of one parent to 
        the next.
        """

        reduce_step = mr.models.kv.step.get(
                        message_parameters.workflow, 
                        parent_invocation.step_name)

        reduce_handler = mr.models.kv.handler.get(
                            message_parameters.workflow, 
                            reduce_step.reduce_handler_name)

        _logger.debug("Queueing reduce of step [%s] for parent invocation: [%s]", 
                      reduce_step.step_name, parent_invocation)

        workflow = message_parameters.workflow

        reduce_invocation = mr.models.kv.invocation.Invocation(
                                invocation_id=None,
                                workflow_name=\
                                    workflow.workflow_name,
                                parent_invocation_id=\
                                    parent_invocation.invocation_id,
                                step_name=reduce_step.step_name,
                                direction=mr.constants.D_REDUCE)

        reduce_invocation.save()

        # Queue the reduction.

        reduce_parameters = mr.shared_types.QUEUE_MESSAGE_PARAMETERS_CLS(
            workflow=workflow,
            invocation=reduce_invocation,
            request=message_parameters.request,
            job=message_parameters.job,
            step=reduce_step,
            handler=reduce_handler)

        assert reduce_parameters.handler is not None

        _logger.debug("Reduction [%s] will be performed over step: [%s].", 
                      reduce_parameters.invocation, reduce_step.step_name)

        if reduce_handler.required_capability != \
                mr.constants.REQUIRED_CAP_NONE:
            capability_name = reduce_handler.required_capability
        else:
            capability_name = mr.constants.CAP_GENERAL

        replacements = {
            'workflow_name': workflow.workflow_name,
            'capability_name': capability_name,
        }

        topic = mr.config.queue.TOPIC_NAME_REDUCE_TEMPLATE % replacements

        self.__q.producer.push_one(
            topic, 
            mr.constants.D_REDUCE, 
            reduce_parameters)

_pusher = None
def _get_pusher():
    global _pusher

    if _pusher is None:
        _pusher = _QueuePusher()

    return _pusher


class _StepProcessor(object):
    """Receives queued items to be processed. We are running in our own gthread 
    by the time we're called.
    """

    def __queue_map_step(self, next_step, kv_tuple, original_parameters):
        request = original_parameters.request
        workflow = original_parameters.workflow
        job = original_parameters.job
        step = original_parameters.step
        parent_map_invocation = original_parameters.invocation

        assert parent_map_invocation.invocation_id is not None

        next_handler = mr.models.kv.handler.get(
                        workflow, 
                        next_step.map_handler_name)

        # The next invocation will have this [mapping] step as a parent.
        map_invocation = mr.models.kv.invocation.Invocation(
                                invocation_id=None,
                                workflow_name=workflow.workflow_name,
                                parent_invocation_id=\
                                    parent_map_invocation.invocation_id,
                                step_name=next_step.step_name,
                                direction=mr.constants.D_MAP)

        map_invocation.save()

        _flow_logger.debug("+ Writing ARGUMENTS dataset from [%s] to "
                           "downstream mapper [%s].",
                           parent_map_invocation, map_invocation)

        # Store the arguments for the new invocation.

        dq = mr.models.kv.queues.dataset.DatasetQueue(
                workflow, 
                map_invocation, 
                mr.models.kv.queues.dataset.DT_ARGUMENTS)

        data = {
            'p': kv_tuple,
        }

        dq.add(data)

        # Track the relationship.

        rt = mr.models.kv.trees.relationships.RelationshipsTree(
                workflow, 
                parent_map_invocation,
                mr.models.kv.trees.relationships.RT_MAPPED)

        rt.add_entity(map_invocation)

        # Queue the mapping.

        mapped_parameters = mr.shared_types.QUEUE_MESSAGE_PARAMETERS_CLS(
            workflow=workflow,
            invocation=map_invocation,
            request=request,
            job=job,
            step=next_step,
            handler=next_handler)

        pusher = _get_pusher()
        pusher.queue_map_step_from_parameters(mapped_parameters)

    def __call_handler(self, workflow, handler_name, arguments):
        wm = mr.workflow_manager.get_wm()
        managed_workflow = wm.get(workflow.workflow_name)
        handlers = managed_workflow.handlers

        _logger.debug("Calling handler [%s] under workflow [%s].", 
                      handler_name, workflow.workflow_name)

        return handlers.run_handler(handler_name, arguments)

    def __default_combiner(self, map_result_gen):
        """The default combiner: group by key."""

        if mr.config.IS_DEBUG is True:
            map_result_gen = list(map_result_gen)
            _logger.debug("Combining (default):\n%s", 
                          pprint.pformat(map_result_gen))

        # itertools.groupby() requires it to be sorted, first.
        sorted_result_gen = (p 
                             for p 
                             in sorted(
                                    map_result_gen, 
                                    key=lambda x: x[0]))

        if mr.config.IS_DEBUG is True:
            sorted_result_gen = list(sorted_result_gen)
            _logger.debug("Pre-combine sort:\n%s",
                          pprint.pformat(sorted_result_gen))

        grouped_result_gen = itertools.groupby(
                                sorted_result_gen, 
                                lambda x: x[0])

        def make_distilled_result_gen():
            for k, value_list in grouped_result_gen:
                yield (k, (v for (_, v) in value_list))

        distilled_result_gen = make_distilled_result_gen()

        if mr.config.IS_DEBUG is True:
            distilled_result_gen = [(k, list(value_list)) 
                                    for (k, value_list) 
                                    in distilled_result_gen]

            _logger.debug("Combiner result:\n%s", 
                          pprint.pformat(distilled_result_gen))

        return distilled_result_gen

    def __apply_combiner(self, workflow, current_step, map_invocation, 
                         map_result_gen):
        combine_handler_name = current_step.combine_handler_name

        handler_ctx = self.__get_handler_context(workflow, map_invocation)

        if combine_handler_name is not None:
            combine_handler = functools.partial(
                                self.__call_handler, 
                                workflow, 
                                combine_handler_name)

            return combine_handler(map_result_gen, handler_ctx)
        else:
            return self.__default_combiner(map_result_gen)

    def __map_to_downstream(self, mapped_step_name, handler_name, 
                            mapped_steps_gen, workflow, invocation, 
                            message_parameters):
        """A mapping step has completed and has mapped into one or more 
        downstream steps. Queue the downstream steps to be handled and tracked.
        """

        assert invocation.mapped_count is None
        assert invocation.mapped_waiting is None

        mapped_step = mr.models.kv.step.get(workflow, mapped_step_name)

        # This has to be an integer just in case one of the downstream steps 
        # completes before we finish our accounting, here.

        invocation.mapped_waiting = 0
        invocation.save()

        i = 0
        for (k, v) in mapped_steps_gen:
            _logger.debug("Queueing mapping (%d) from invocation [%s].",
                          i, invocation)

            self.__queue_map_step(
                    mapped_step, 
                    (k, v), 
                    message_parameters)

            i += 1

        step_count = i

        # Now, update the number of mapped steps into the invocation. 
        #
        # Because we either decrement or add maximum positive value, and the 
        # value of mapped_waiting will never be glimpsed before decrementing 
        # it, there won't be any chance of a completed step seeing the 
        # mappd_waiting value equal zero more than once (which is our trigger 
        # for a reduction), which will be the very last manipulation it 
        # counters.

        _logger.debug("Invocation [%s] has mapped (%d) steps.", 
                      invocation, step_count)

# TODO(dustin): We might need to check for whether a reduction is necessary 
#               here. By the time we get here, we could've potentially finished 
#               all steps, which nothing else checking for (0) waiting-steps.

        invocation = self.__add_mapped_steps(
                        workflow, 
                        invocation, 
                        step_count)

        _logger.debug("Invocation [%s] has had its counts updated: MC=(%d) "
                      "MW=(%d)", 
                      invocation, invocation.mapped_count, 
                      invocation.mapped_waiting)

    def __map_collect_result(self, handler_name, handler_result_gen, workflow, 
                             invocation, message_parameters):
        """The mapper returned a generator of key-value pairs (rather than 
        mapping to another downstream step). This is essentially an invocation
        "leaf" that will end any branching activity, and either contribute one
        child of a step that mapped or complete the request.
        """

        # Wrap the result generator in a combiner generator. By the time we get 
        # the data, it'll already be combined.
        #
        # This ensures that we have the opportunity to flatten the data between 
        # descending map operations. Note that the default combiner groups by 
        # key, but does not flatten the value (concatenation, summing, etc..). 
        # So, descending maps will be grouped, grouped a second time, grouped a 
        # third time, etc.. It's probably almost always desired to provide a 
        # combiner if we have more than one dimension of steps.
        map_result_gen = self.__apply_combiner(
                            workflow, 
                            message_parameters.step, 
                            invocation,
                            handler_result_gen)

        _logger.debug("Writing result-set for invocation: [%s]", invocation)

        _flow_logger.debug("+ Writing POST-COMBINE dataset received from "
                           "mapper to itself: [%s]", invocation)

        dq = mr.models.kv.queues.dataset.DatasetQueue(
                workflow, 
                invocation,
                mr.models.kv.queues.dataset.DT_POST_COMBINE)

        if mr.config.IS_DEBUG is True:
            map_result_gen = [(k, list(v)) for (k, v) in map_result_gen]
            _logger.debug("Result to be stored:\n%s", 
                          pprint.pformat(map_result_gen))

        i = 0
        for (k, value_list) in map_result_gen:
            data = { 
                'k': k,
                'vl': list(value_list),
            }

            dq.add(data)
            i += 1

        _logger.debug("Result-set of size (%d) written for invocation [%s]. "
                      "Queueing reduction.", i, invocation)

        # We're here because a map operation rendered a result (and did not map 
        # further downstream). It's tempting to want to reduce here, but we'd 
        # end up compromising the whole concept of map-reduce, and we might 
        # potential be processing a high-cost mapping *and* a high-cost 
        # reduction within the same invocation.

        pusher = _get_pusher()

        # Do a reduction with this invocation as the parent (it will access our 
        # results).
        pusher.queue_reduce_step_from_parameters(
            message_parameters, 
            invocation)

    def __get_handler_context(self, workflow, map_invocation, 
                              allow_session_writes=True):
        """Return accessors of data that's stored on the map_invocation."""

        st = mr.models.kv.trees.sessions.SessionsTree(
                workflow, 
                map_invocation)

        state = { 'verified': None }

        def check_state():
            # Determine if the tree needs to be created, lazily (it might have 
            # not been used).
            if state['verified'] is None:
                if st.exists() is False:
                    _logger.debug("Creating session for map-invocation: %s", 
                                  map_invocation)

                    try:
                        st.create()
                    except mr.models.kv.data_layer.KvPreconditionException:
                        _logger.warning("It looks like the session was "
                                        "already started by a parallel "
                                        "mechanism.")
                else:
                    _logger.debug("Session for map-invocation already exists: "
                                  "%s", map_invocation)

                state['verified'] = True

        def session_set_accessor(key, value):
            if allow_session_writes is False:
                raise EnvironmentError("Session writes are disabled from the "
                                       "current context.")

            check_state()
            st.set(key, value)

        def session_get_accessor(key):
            check_state()
            return st.get(key)

        def session_list_accessor():
            check_state()
            return st.list()

# TODO(dustin): We still have to implement the "STEP_INSTANCE_ID" field.
#                'STEP_INSTANCE_ID': 1234,

        return HANDLER_CTX_CLS(
                session_get=session_get_accessor, 
                session_set=session_set_accessor,
                session_list=session_list_accessor)

    def handle_map(self, message_parameters):
        """Handle one dequeued map job."""

        request = message_parameters.request
        step = message_parameters.step
        invocation = message_parameters.invocation
        workflow = message_parameters.workflow
        
        _logger.debug("Processing MAP: [%s]", invocation)

        try:
            ## Call the handler.

            _flow_logger.debug("  Reading ARGUMENTS dataset for (and from) "
                               "mapper: [%s]", invocation)

            dq = mr.models.kv.queues.dataset.DatasetQueue(
                    workflow, 
                    invocation, 
                    mr.models.kv.queues.dataset.DT_ARGUMENTS)

            # Enumerate the 'p' member of every record.
            arguments = (d['p'] for d in dq.list_data())

            if mr.config.IS_DEBUG is True:
                arguments = list(arguments)
                _logger.debug("Sending arguments to mapper:\n%s", 
                              pprint.pformat(arguments))

            handler_ctx = self.__get_handler_context(workflow, invocation)

            wrapped_arguments = {
                'arguments': arguments,
                'ctx': handler_ctx,
            }

            handler_result_gen = self.__call_handler(
                                    workflow, 
                                    step.map_handler_name, 
                                    wrapped_arguments)

            path_type = next(handler_result_gen)

            _logger.debug("Mapper [%s] path-type: [%s]", 
                          invocation, path_type.__class__.__name__)

            assert issubclass(
                    path_type.__class__, 
                    mr.handlers.scope.MrConfigure) is True

            # Manage downstream steps that were mapped to (the handler was a 
            # generator).

            if issubclass(
                   path_type.__class__, 
                   mr.handlers.scope.MrConfigureToMap) is True:

                self.__map_to_downstream(
                    path_type.next_step_name,
                    step.map_handler_name, 
                    handler_result_gen,
                    workflow, 
                    invocation, 
                    message_parameters)
            elif issubclass(
                    path_type.__class__, 
                    mr.handlers.scope.MrConfigureToReturn) is True:

                self.__map_collect_result(
                    step.map_handler_name,
                    handler_result_gen,
                    workflow, 
                    invocation,
                    message_parameters)
        except:
            _logger.exception("Exception while processing MAP under request: "
                              "%s", request)

# TODO(dustin): We might have to remove the chain of invocations, on error.
            invocation.error = traceback.format_exc()
            invocation.save()

            request.failed_invocation_id = invocation.invocation_id
            request.done = True
            request.save()

            raise

    def __decrement_invocation(self, workflow, invocation):
        def get_cb():
            obj = mr.models.kv.invocation.get(
                    workflow, 
                    invocation.invocation_id)

            return obj

        def set_cb(obj):
            obj.mapped_waiting -= 1

        obj = mr.models.kv.invocation.Invocation.atomic_update(get_cb, set_cb)
        return obj

    def __add_mapped_steps(self, workflow, invocation, step_count):
        def get_cb():
            return mr.models.kv.invocation.get(
                    workflow, 
                    invocation.invocation_id)

        def set_cb(obj):
            obj.mapped_count = step_count
            obj.mapped_waiting += step_count

        return mr.models.kv.invocation.Invocation.atomic_update(get_cb, set_cb)

    def handle_reduce(self, message_parameters):
        """Corresponds to steps received with a type of mr.constants.D_REDUCE.

        As we work our way down from the request/job/original-step to 
        successive mappings, we link them by way of the parent_invocation_id.
        When we're working our way up through reduction, the 
        parent_invocation_id of each reduction invocation points to the 
        invocation record that we're reducing. We'll then continue to queue 
        successive invocation for the parents of parents, until we make it all
        of the way to the original step (which will have no parent).
        """

        step = message_parameters.step
        reduce_invocation = message_parameters.invocation
        workflow = message_parameters.workflow
        request = message_parameters.request

        assert step.reduce_handler_name is not None

        try:
            # The parent of the current invocation is the invocation that had all 
            # of the mappings to be reduced.

            map_invocation = mr.models.kv.invocation.get(
                                workflow, 
                                reduce_invocation.parent_invocation_id)

            if map_invocation.mapped_waiting is None:
                _logger.debug("Processing REDUCE [%s] -of- original MAP "
                              "invocation [%s] that rendered a DATASET.",
                              reduce_invocation, map_invocation)

                return self.__handle_mapped_dataset_reduce(
                        message_parameters,
                        step, 
                        map_invocation,
                        workflow, 
                        request)
            else:
                _logger.debug("Processing REDUCE [%s] -of- original MAP "
                              "invocation [%s] that rendered DOWNSTREAM "
                              "MAPPINGS.",
                              reduce_invocation, map_invocation)

                return self.__handle_mapped_mapping_reduce(
                        message_parameters,
                        step, 
                        map_invocation,
                        workflow, 
                        request)
        except:
            _logger.exception("Exception while processing REDUCE under "
                              "request: %s", request)

# TODO(dustin): We might have to remove the chain of invocations, on error.
            reduce_invocation.error = traceback.format_exc()
            reduce_invocation.save()

            request.failed_invocation_id = reduce_invocation.invocation_id
            request.done = True
            request.save()

            raise

    def __handle_mapped_mapping_reduce(self, message_parameters, step, 
                                       map_invocation, workflow, request):
        """Reduce over a mapping invocation that rendered a dataset."""

        # Call the handler with a generator of all of the results to be 
        # reduced.

        _flow_logger.debug("  Reading POST-COMBINE datasets for [%s] from "
                           "downstream mappings.", 
                           message_parameters.invocation)

        def get_results_gen():
            """Enumerate all (key, value_list) from all results of all 
            invocations mapped from this invocation.

            Note that, no matter how good the combiner is, if one step maps 
            into downstream steps than there could very well have duplicate 
            keys (which is a relatively normal circumstance, but entirely 
            unavoidable of multidimensional-mappings).
            """

            _logger.debug("Aggregating results of mapping: [%s]", 
                          map_invocation)

            parent_tree = mr.models.kv.trees.relationships.RelationshipsTree(
                            workflow, 
                            map_invocation,
                            mr.models.kv.trees.relationships.RT_MAPPED)

            for mapped_invocation in parent_tree.list_entities():
                # A relationship of each of the datasets being reduced to the 
                # invocation that we're pushing it to.

                rt = mr.models.kv.trees.relationships.RelationshipsTree(
                        workflow, 
                        mapped_invocation,
                        mr.models.kv.trees.relationships.RT_REDUCED)

                # Store the reduction's invocation ID.
                
                data = {
                    'ri': message_parameters.invocation.invocation_id,
                }
                
                rt.add_entity(map_invocation, data=data)

                # Yield through the reduction datasets of each of the mappings 
                # that we branched to.

                _flow_logger.debug("  Reading constituent POST-REDUCE result "
                                   "for parent [%s] by [%s] from: [%s]", 
                                   map_invocation, 
                                   message_parameters.invocation, 
                                   mapped_invocation)

                dq = mr.models.kv.queues.dataset.DatasetQueue(
                        workflow, 
                        mapped_invocation,
                        mr.models.kv.queues.dataset.DT_POST_REDUCE)

                for data in dq.list_data():
                    yield data

        results_gen = get_results_gen()

        if mr.config.IS_DEBUG is True:
            results_gen = list(results_gen)

            _logger.debug("(%d) results will be reduced by step [%s] for "
                          "original invocation [%s].",
                          len(results_gen), step.reduce_handler_name, 
                          map_invocation)

            print('')
            for (i, data) in enumerate(results_gen):
                (k, v) = data['p']
                print("Result (%d)\nKey: %s\n Value: %s" % 
                      (i, k, v))

            print('')

        results_gen = (data['p'] for data in results_gen)

        # Disable session writes because there's no purpose by the time we get 
        # to the reducer.
        handler_ctx = self.__get_handler_context(
                        workflow, 
                        map_invocation, 
                        allow_session_writes=False)

        handler_arguments = {
            'results': results_gen,
            'ctx': handler_ctx,
        }

        reduce_result_gen = self.__call_handler(
                                workflow,
                                step.reduce_handler_name, 
                                handler_arguments)

        if mr.config.IS_DEBUG is True:
            reduce_result_gen = list(reduce_result_gen)            
            _logger.debug("Handler [%s] reduction [%s] result:\n%s", 
                          step.reduce_handler_name, map_invocation,
                          pprint.pformat(reduce_result_gen))

        if map_invocation.parent_invocation_id is not None:
            decrement_invocation = mr.models.kv.invocation.get(
                                    workflow, 
                                    map_invocation.parent_invocation_id)
        else:
            decrement_invocation = None

        self.__store_reduction_result(
            message_parameters,
            reduce_result_gen, 
            map_invocation,
            decrement_invocation=decrement_invocation)

    def __handle_mapped_dataset_reduce(self, message_parameters, step, 
                                       map_invocation, workflow, request):
        """Reduce over a mapping invocation that mapped to downstream steps."""

        _logger.debug("Reducing over mapped results of mapper: [%s]", 
                      map_invocation)

        _flow_logger.debug("  Reading POST-COMBINE dataset from [%s] returned "
                           "by mapper: [%s]", 
                           message_parameters.invocation, map_invocation)

        # Establish the dataset that was rendered by the one map.

        dq = mr.models.kv.queues.dataset.DatasetQueue(
                workflow, 
                map_invocation,
                mr.models.kv.queues.dataset.DT_POST_COMBINE)

        results_gen = dq.list_data()

        if mr.config.IS_DEBUG is True:
            results_gen = list(results_gen)

            _logger.debug("(%d) results will be reduced by step [%s] for "
                          "original invocation [%s].",
                          len(results_gen), step.reduce_handler_name, 
                          map_invocation)
            
            print('')
            for (i, data) in enumerate(results_gen):
                print("Result (%d)\nKey: %s\n Value List: %s" % 
                      (i, data['k'], data['vl']))

            print('')

        # A relationship of us *to* us to indicate that the mapping produced 
        # data directly, and that data was reduced directly.

        rt = mr.models.kv.trees.relationships.RelationshipsTree(
                workflow, 
                map_invocation,
                mr.models.kv.trees.relationships.RT_REDUCED)

        # Store the reduction's invocation ID.

        data = {
            'ri': message_parameters.invocation.invocation_id,
        }
        
        rt.add_entity(map_invocation, data=data)

        results_gen = ((data['k'], data['vl']) for data in results_gen)

        # Disable session writes because there's no purpose by the time we get 
        # to the reducer.
        handler_ctx = self.__get_handler_context(
                        workflow, 
                        map_invocation, 
                        allow_session_writes=False)

        handler_arguments = {
            'results': results_gen,
            'ctx': handler_ctx,
        }

        # Call the handler with a generator of all of the results to be 
        # reduced.

        reduce_result_gen = self.__call_handler(
                                workflow,
                                step.reduce_handler_name, 
                                handler_arguments)

        if mr.config.IS_DEBUG is True:
            reduce_result_gen = list(reduce_result_gen)            
            _logger.debug("Handler [%s] reduction [%s] result:\n%s", 
                          step.reduce_handler_name, map_invocation, 
                          pprint.pformat(reduce_result_gen))

        if map_invocation.parent_invocation_id is not None:
            decrement_invocation = mr.models.kv.invocation.get(
                                    workflow, 
                                    map_invocation.parent_invocation_id)
        else:
            decrement_invocation = None

        self.__store_reduction_result(
            message_parameters,
            reduce_result_gen, 
            map_invocation,
            decrement_invocation=decrement_invocation)

    def __store_reduction_result(self, message_parameters, reduce_result_gen,
                                 store_to_invocation, 
                                 decrement_invocation=None):
        """Store the reduction result. This is code common to both/all kinds of 
        reduction.
        """

        workflow = message_parameters.workflow
        request = message_parameters.request

        # Store result

        _logger.debug("Writing reduction result: [%s] [%s]", 
                      store_to_invocation, store_to_invocation.direction)

        _flow_logger.debug("+ Writing POST-REDUCE dataset from [%s] to [%s] "
                           "and decrementing [%s].",
                           message_parameters.invocation, store_to_invocation,
                           decrement_invocation)

        dq = mr.models.kv.queues.dataset.DatasetQueue(
                workflow, 
                store_to_invocation,
                mr.models.kv.queues.dataset.DT_POST_REDUCE)

        i = 0
        for (k, v) in reduce_result_gen:
            data = {
                # Pair
                'p': (k, v),
            }

            dq.add(data)
            i += 1

        assert i > 0, "No reduction results to store by [%s] to [%s]." % \
                      (message_parameters.invocation, store_to_invocation)

        _logger.debug("We've posted the reduction result to invocation: "
                      "[%s]", store_to_invocation)

        if decrement_invocation is not None:
            _logger.debug("Decrementing invocation: [%s] WAITING=(%d)",
                          decrement_invocation,
                          decrement_invocation.mapped_waiting)

            # Decrement the "waiting" counter on the parent of the parent 
            # (the step that mapped the steps that produced the results 
            # that we're reducing), or notify that the job is done (if 
            # there is no parent's parent).

            decrement_invocation = self.__decrement_invocation(
                                    workflow, 
                                    decrement_invocation)

            if decrement_invocation.mapped_waiting == 0:
                # We've posted the reduction of the results of our map step 
                # to its parent, and all mapped steps of that parent have 
                # now been reported.

                _logger.debug("Invocation [%s] mapped-waiting count has "
                              "dropped to (0), and will be reduced.", 
                              decrement_invocation)

                pusher = _get_pusher()

                # Queue a reduction with our parent's parent (the parent of 
                # the original mapping). It will access all of the results 
                # that have been posted back to it.
                pusher.queue_reduce_step_from_parameters(
                    message_parameters, 
                    decrement_invocation)
            else:
                _logger.debug("Invocation [%s] mapped-waiting "
                              "count after REDUCE: (%d)", 
                              decrement_invocation,
                              decrement_invocation.mapped_waiting)
        else:
            # We've reduced our way back up to the original request.

            _logger.debug("No further parents. Marking request as "
                          "complete: [%s]", request.request_id)

            request.done = True
            request.save()

_sp = _StepProcessor()

def get_step_processor():
    return _sp


class _RequestReceiver(object):
    """Receives the web-requests to push new job requests."""

    def __init__(self):
        self.__q = mr.queue.queue_manager.get_queue()

        result_writer_cls = mr.utility.load_cls_from_string(
                                mr.config.result.RESULT_WRITER_FQ_CLASS)

        self.__result_writer = result_writer_cls()

    def __push_request(self, message_parameters):
        pusher = _get_pusher()
        pusher.queue_initial_map_step_from_parameters(message_parameters)

    def __block_for_result(self, message_parameters):
        request = message_parameters.request

        _logger.debug("Blocking on result for request: [%s]", 
                      request.request_id)

        # The object is replaced with a newer one, when a change happens.
        request = request.wait_for_change()

        _logger.debug("Reading result from: [%s] [%s]",
                      message_parameters.invocation,
                      message_parameters.invocation.direction)

        _flow_logger.debug("  Reading POST-REDUCE dataset as final result: "
                           "[%s]", message_parameters.invocation)

        dq = mr.models.kv.queues.dataset.DatasetQueue(
                message_parameters.workflow, 
                message_parameters.invocation, 
                mr.models.kv.queues.dataset.DT_POST_REDUCE)

        result_pair_gen = (d['p'] for d in dq.list_data())

        if mr.config.IS_DEBUG is True:
            result_pair_gen = list(result_pair_gen)
            _logger.debug("Result to return for request:\n%s", 
                          pprint.pformat(result_pair_gen))

        return self.__result_writer.get_response_tokens(
                request.request_id, 
                result_pair_gen)

    def package_request(self, workflow, job, step, handler, arguments, 
                        context):
        """Prepare an incoming request to be processed."""

        invocation = mr.models.kv.invocation.Invocation(
                        invocation_id=None,
                        workflow_name=workflow.workflow_name,
                        step_name=step.step_name,
                        direction=mr.constants.D_MAP)

        invocation.save()

        _flow_logger.debug("+ Writing ARGUMENTS dataset for root invocation: "
                           "[%s]", invocation)

        dq = mr.models.kv.queues.dataset.DatasetQueue(
                workflow, 
                invocation,
                mr.models.kv.queues.dataset.DT_ARGUMENTS)

        for (k, v) in arguments:
            data = {
                'p': (k, v),
            }

            dq.add(data)

        request = mr.models.kv.request.Request(
                    request_id=None,
                    workflow_name=workflow.workflow_name,
                    job_name=job.job_name, 
                    invocation_id=invocation.invocation_id,
                    context=context)

        request.save()

        _logger.debug("Received request: [%s]", request)

        message_parameters = mr.shared_types.QUEUE_MESSAGE_PARAMETERS_CLS(
                                workflow=workflow,
                                invocation=invocation,
                                request=request,
                                job=job, 
                                step=step,
                                handler=handler)

        return message_parameters

    def process_request(self, message_parameters):
        self.__push_request(message_parameters)
        r = self.__block_for_result(message_parameters)

        return r

_request_receiver = None
def get_request_receiver():
    global _request_receiver

    if _request_receiver is None:
        _request_receiver = _RequestReceiver()

    return _request_receiver
