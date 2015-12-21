
from hybrid_cloud.scheduler.oslib import loadables


class BaseFilter(object):
    """Base class of all filter classes."""
    def _filter_one(self, obj, filter_properties):
        """Return True if it passes the filter, False otherwise.
        Override this in a subclass.
        """
        return True

    def filter_all(self, filter_obj_list, filter_properties):
        """Yield objects that pass the filter.

        Can be overridden in a subclass, if you need to base filtering
        decisions on all objects.  Otherwise, one can just override
        _filter_one() to filter a single object.
        """

        for obj in filter_obj_list:
            if self._filter_one(obj, filter_properties):
                yield obj

    # Set to true in a subclass if a filter only needs to be run once
    # for each request rather than for each instance
    run_filter_once_per_request = False

    def run_filter_for_index(self, index):
        """Return True if the filter needs to be run for the "index-th"
        instance in a request.  Only need to override this if a filter
        needs anything other than "first only" or "all" behaviour.
        """
        if self.run_filter_once_per_request and index > 0:
            return False
        else:
            return True


class BaseFilterHandler(loadables.BaseLoader):
    """Base class to handle loading filter classes.

    This class should be subclassed where one needs to use filters.
    """

    def get_filtered_objects(self, filters, objs, filter_properties, index=0):

        list_objs = list(objs)

        #LOG.debug("Starting with %d host(s)", len(list_objs))
        # Track the hosts as they are removed. The 'full_filter_results' list
        # contains the host/nodename info for every host that passes each
        # filter, while the 'part_filter_results' list just tracks the number
        # removed by each filter, unless the filter returns zero hosts, in
        # which case it records the host/nodename for the last batch that was
        # removed. Since the full_filter_results can be very large, it is only
        # recorded if the LOG level is set to debug.
        # part_filter_results = []
        # full_filter_results = []
        # log_msg = "%(cls_name)s: (start: %(start)s, end: %(end)s)"


        for filter_ in filters:
            if filter_.run_filter_for_index(index):
                # cls_name = filter_.__class__.__name__
                # start_count = len(list_objs)
                objs = filter_.filter_all(list_objs, filter_properties)

                if objs is None:
                    # LOG.debug("Filter %s says to stop filtering", cls_name)
                    return []
                list_objs = list(objs)
                #end_count = len(list_objs)
                #part_filter_results.append(log_msg % {"cls_name": cls_name,
                #        "start": start_count, "end": end_count})
                #if list_objs:
                #    remaining = [(getattr(obj, "host", obj),
                #                  getattr(obj, "nodename", ""))
                #                 for obj in list_objs]
                #    full_filter_results.append((cls_name, remaining))
                #else:
                #    LOG.info(_LI("Filter %s returned 0 hosts"), cls_name)
                #    full_filter_results.append((cls_name, None))
                #    break
                # LOG.debug("Filter %(cls_name)s returned "
                #           "%(obj_len)d host(s)",
                #           {'cls_name': cls_name, 'obj_len': len(list_objs)})


        #
        # Logger
        #
        #
        # if not list_objs:
        #     # Log the filtration history
        #     rspec = filter_properties.get("request_spec", {})
        #     inst_props = rspec.get("instance_properties", {})
        #     msg_dict = {"res_id": inst_props.get("reservation_id", ""),
        #                 "inst_uuid": inst_props.get("uuid", ""),
        #                 "str_results": str(full_filter_results),
        #                }
        #     full_msg = ("Filtering removed all hosts for the request with "
        #                 "reservation ID '%(res_id)s' and instance ID "
        #                 "'%(inst_uuid)s'. Filter results: %(str_results)s"
        #                ) % msg_dict
        #     msg_dict["str_results"] = str(part_filter_results)
        #     part_msg = _LI("Filtering removed all hosts for the request with "
        #                    "reservation ID '%(res_id)s' and instance ID "
        #                    "'%(inst_uuid)s'. Filter results: %(str_results)s"
        #                    ) % msg_dict
        #     LOG.debug(full_msg)
        #     LOG.info(part_msg)
        return list_objs
