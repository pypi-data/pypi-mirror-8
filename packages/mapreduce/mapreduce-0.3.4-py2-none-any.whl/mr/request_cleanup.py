import logging
import pprint
import threading
import Queue

import mr.config
import mr.config.request
import mr.trace
import mr.models.kv.workflow
import mr.models.kv.queues.dataset
import mr.models.kv.trees.relationships
import mr.models.kv.trees.sessions

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.WARNING)


class RequestCleanup(object):
    """Cleanup all traces of a request."""

    def __init__(self, request, just_simulate=False):
        self.__request = request
        self.__workflow = mr.models.kv.workflow.get(request.workflow_name)
        self.__just_simulate = just_simulate

    def __prune_invocation_data(self, invocation):
        """Remove associated datasets."""

        # Remove argument data.

        try:
            dqa = mr.models.kv.queues.dataset.DatasetQueue(
                    self.__workflow, 
                    invocation,
                    mr.models.kv.queues.dataset.DT_ARGUMENTS)

            if self.__just_simulate is True:
                list(dqa.list())
            else:
                dqa.delete()
        except KeyError:
            _logger.debug("No ARGUMENT datasets to be removed for invocation: "
                          "[%s]", invocation.invocation_id)
        else:
            _logger.debug("Removed ARGUMENT datasets for invocation: [%s]", 
                          invocation.invocation_id)

        # Remove post-combine data.

        try:
            dqc = mr.models.kv.queues.dataset.DatasetQueue(
                    self.__workflow, 
                    invocation,
                    mr.models.kv.queues.dataset.DT_POST_COMBINE)

            if self.__just_simulate is True:
                list(dqc.list())
            else:
                dqc.delete()
        except KeyError:
            _logger.debug("No POST-COMBINE datasets to be removed for invocation: "
                          "[%s]", invocation.invocation_id)
        else:
            _logger.debug("Removed POST-COMBINE datasets for invocation: [%s]", 
                          invocation.invocation_id)

        # Remove post-reduce data.

        try:
            dqr = mr.models.kv.queues.dataset.DatasetQueue(
                    self.__workflow, 
                    invocation,
                    mr.models.kv.queues.dataset.DT_POST_REDUCE)

            if self.__just_simulate is True:
                list(dqr.list())
            else:
                dqr.delete()
        except KeyError:
            _logger.debug("No POST-REDUCE datasets to be removed for invocation: "
                          "[%s]",
                          invocation.invocation_id)
        else:
            _logger.debug("Removed POST-REDUCE datasets for invocation: [%s]", 
                          invocation.invocation_id)

    def __prune_invocation_relationships(self, invocation):
        """Remove the associated relationship paper-trail."""

        try:
            mrt = mr.models.kv.trees.relationships.RelationshipsTree(
                    self.__workflow, 
                    invocation, 
                    mr.models.kv.trees.relationships.RT_MAPPED)

            if self.__just_simulate is True:
                list(mrt.list())
            else:
                mrt.delete()
        except KeyError:
            _logger.debug("No MAPPED relationships to remove for invocation: "
                          "[%s]", invocation.invocation_id)
        else:
            _logger.debug("Removed MAPPED relationships: [%s]", 
                          invocation.invocation_id)

        try:
            rrt = mr.models.kv.trees.relationships.RelationshipsTree(
                    self.__workflow, 
                    invocation, 
                    mr.models.kv.trees.relationships.RT_REDUCED)

            if self.__just_simulate is True:
                list(rrt.list())
            else:
                rrt.delete()
        except KeyError:
            _logger.debug("No REDUCED relationships to remove for invocation: "
                          "[%s]", invocation.invocation_id)
        else:
            _logger.debug("Removed REDUCED relationships: [%s]", 
                          invocation.invocation_id)

    def __prune_invocation_sessions(self, map_invocation):
        """Remove the session-data associated with the mapping-invocation."""

        try:
            st = mr.models.kv.trees.sessions.SessionsTree(
                    self.__workflow, 
                    map_invocation)

            if self.__just_simulate is True:
                list(st.list())
            else:
                st.delete()
        except KeyError:
            _logger.debug("No sessions to remove for invocation: "
                          "[%s]", map_invocation.invocation_id)
        else:
            _logger.debug("Removed sessions: [%s]", 
                          map_invocation.invocation_id)

    def __prune_invocation(self, invocation):
        self.__prune_invocation_data(invocation)
        self.__prune_invocation_relationships(invocation)

        if invocation.direction == mr.constants.D_MAP:
            self.__prune_invocation_sessions(invocation)

        if self.__just_simulate is True:
            _logger.debug("SIMULATION: Not removing invocation: %s", 
                          invocation)
        else:
            _logger.debug("Removing invocation: %s", str(invocation))
            invocation.delete()

    def prune_request(self):
        _logger.info("Pruning request: [%s]", self.__request.request_id)

        # Compile a list of invocations. We'd prefer to start deleting at the 
        # leafs, but we are dealing with a graph, and not a tree, and the 
        # relationships are a bit too complicated.

        invocations = {}

        try:
            for (child_invocation, parent_invocation, is_loop_to_self) \
                in mr.trace.invocation_graph_gen(self.__workflow, self.__request):
                    invocations[child_invocation.invocation_id] = child_invocation

                    if parent_invocation is not None:
                        invocations[parent_invocation.invocation_id] = \
                            parent_invocation
        except mr.trace.InvocationLookupError:
# TODO(dustin): We might try to recover from this, either inside the tracer or 
#               using an alternative, recovery-oriented mechanism.
            _logger.warning("It looks like a previous prune may have been "
                            "interrupted. There was a problem identifying "
                            "records to cleanup for request [%s].", 
                            str(self.__request))

        if mr.config.IS_DEBUG is True:
            _logger.debug("(%d) invocations to be pruned:\n%s", 
                          len(invocations), pprint.pformat(invocations.keys()))

        # Delete the invocations.

        for (invocation_id, invocation) in invocations.iteritems():
            self.__prune_invocation(invocation)

        # Now, delete the request.

        if self.__just_simulate is True:
            _logger.debug("SIMULATION: Not removing request: %s", 
                          str(self.__request))
        else:
            _logger.debug("Removing request.")
            self.__request.delete()


class CleanupQueue(object):
    """A cleanup-manager that runs in its own thread."""

    def __init__(self, workflow):
        self.__workflow = workflow
        self.__q = Queue.Queue()

        self.__cc_exit_ev = threading.Event()
        self.__cc_t = None

        _logger.debug("Checking whether request cleanup-queue currently "
                      "exists.")

        if mr.config.request.DO_CLEANUP_REQUESTS is True:
            self.__schedule_cleanup_check()
        else:
            _logger.warning("Request cleanup is disabled. Not scheduling "
                            "cleanup thread.")

    def __del__(self):
        if self.__cc_t is not None and self.__cc_t.is_alive() is True:
            self.__cc_exit_ev.set()
            self.__cc_t.join()

    def __schedule_cleanup_check(self):
        self.__cc_t = threading.Thread(target=self.__cleanup_check)
        self.__cc_t.start()

    def __cleanup_check(self):
# TODO(dustin): Add a failsafe mechanism that will allow us to still cleanup 
#               old requests if we're terminated and restarted, or if one 
#               server is docommissioned.

        while self.__cc_exit_ev.is_set() is False:
            _logger.debug("Checking for requests to be pruned.")

            timeout_s = mr.config.request.CLEANUP_TIMEOUT_S

            try:
                request_id = self.__q.get(timeout=timeout_s)
            except Queue.Empty:
                continue

            _logger.debug("Pruning request: %s", request_id)

            try:
                request = mr.models.kv.request.get(
                            self.__workflow, 
                            request_id)
            except KeyError:
                # This shouldn't happen.
                _logger.error("Could not prune request (not found). It "
                              "might've already been removed.")
            else:
                rc = RequestCleanup(request)
                rc.prune_request()

    def add_request(self, request):
        _logger.debug("Adding request to be cleaned-up: %s", str(request))
        self.__q.put(request.request_id)
