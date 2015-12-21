
import random
import logging
logging.basicConfig(filename='./log_yf.txt', level=logging.DEBUG)

from hybrid_cloud.scheduler.oslib import scheduler
from hybrid_cloud.scheduler.cloud_scheduler import filters


CONF_subset_size = 1
CONF_mark_cls_map =\
    {
        'cpu': 'CPUFilter',
        'disk_gb': 'DiskFilter',
        'ram_mb': 'RamFilter',
        'force': 'ForceFilter',
        'ignore': 'IgnoreFilter',
        'price': 'PriceFilter',
    }


class CloudFilterScheduler(scheduler.BaseCloudScheduler):
    """Scheduler that can be used for filtering and weighing."""
    def __init__(self):

        logging.debug('CloudFilterScheduler __init start ...')

        super(CloudFilterScheduler, self).__init__()
        self.filter_handler = filters.CloudFilterHandler()
        filter_classes = self.filter_handler.all_filters()

        self.filter_cls_map = {cls.__name__: cls for cls in filter_classes}
        self.filter_obj_map = {}

        self.mark_cls_map = CONF_mark_cls_map

        logging.debug('CloudFilterScheduler __init end ...')

        # TODO: weight
        #self.weight_handler =




    def select_destinations(self, context, request_spec, filter_properties):
        """Select a filtered cloud"""

        # Multi-create ABANDONED
        # num_instance = request_spec.get('num_instance', 1)
        selected_clouds = self._schedule(context, request_spec, filter_properties)

        if not selected_clouds:
            return {}

        # Choose a cloud randomly from top scheduler_cloud_subset_size cloud
        scheduler_cloud_subset_size = CONF_subset_size
        if scheduler_cloud_subset_size > len(selected_clouds):
            scheduler_cloud_subset_size = len(selected_clouds)
        if scheduler_cloud_subset_size < 1:
            scheduler_cloud_subset_size = 1

        ret_cloud = random.choice(selected_clouds[0: scheduler_cloud_subset_size])

        return ret_cloud

    def _schedule(self, context, request_spec, filter_properties):
        """Returns a list of clouds that meet the required specs,
        ordered by their fitness.
        """
        clouds = self._get_all_cloud_states(None)
        selected_clouds = []

        # Multi-create ABANDONED
        # num_instance = request_spec.get('num_instance', 1)
        # Filter clouds based on requirements ...

        clouds = self._get_filtered_clouds(clouds, filter_properties)

        if not clouds:
            # Can't get any more
            return []

        weighed_clouds = self._get_weighed_clouds(clouds, filter_properties)

        return weighed_clouds

    def _get_all_cloud_states(self, context):
        return self.cloud_state_manager.get_all_cloud_states()

    def _get_filtered_clouds(self, clouds, filter_properties):
        """Filter hosts and return only ones passing all filters."""

        # analyse filter_properties to get filter class names
        filter_class_names = []
        for mark in filter_properties.keys():
            if not self.mark_cls_map.get(mark):
                raise Exception('mark %s is not in mark_cls_map.' % mark)
            if filter_properties.get(mark):
                filter_class_names.append(self.mark_cls_map.get(mark))

        filters = self._choose_cloud_filters(filter_class_names)

        return self.filter_handler.get_filtered_objects(filters,clouds,filter_properties)

    def _get_weighed_clouds(self, clouds, weight_properties):
        """Weigh the clouds, NOT finished yet"""
        # TODO: finished this method
        return clouds

    def _choose_cloud_filters(self, filter_cls_names):
        """Since the caller may specify which filters to use we need
        to have an authoritative list of what is permissible. This
        function checks the filter names against a predefined set
        of acceptable filters.
        """
        if not isinstance(filter_cls_names, (list, tuple)):
            filter_cls_names = [filter_cls_names]

        good_filters = []
        bad_filters = []
        for filter_name in filter_cls_names:
            if filter_name not in self.filter_obj_map:
                if filter_name not in self.filter_cls_map:
                    bad_filters.append(filter_name)
                    continue
                filter_cls = self.filter_cls_map[filter_name]
                self.filter_obj_map[filter_name] = filter_cls()
            good_filters.append(self.filter_obj_map[filter_name])
        if bad_filters:
            msg = ", ".join(bad_filters)
            raise Exception('SchedulerHostFilterNotFound: filter_name = ', msg)
        return good_filters