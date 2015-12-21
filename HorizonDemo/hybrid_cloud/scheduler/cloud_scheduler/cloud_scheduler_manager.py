
from hybrid_cloud.scheduler.cloud_scheduler import cloud_filter_scheduler

import logging
logging.basicConfig(filename='./log_yf.txt', level=logging.DEBUG)


class CloudSchedulerManager(object):
    """Chooses a cloud and one of its host to run instances on."""

    def __init__(self):
        logging.debug('CloudSchedulerManager.__init__ start ...')
        self.filter_scheduler = cloud_filter_scheduler.CloudFilterScheduler()
        self.filter_properties = {}
        logging.debug('CloudSchedulerManager.__init__ end ...')



    def select_cloud(self, request):
        """Returns cloud(s) best suited for this request.
        The result should be a list of cloud.
        """

        # resolve request

        #########################################
        # new structure of filter_property --yufei 2015-12-10 21:51:15
        #########################################
        for key in request.get('flavor'):
            self.filter_properties[key] = request.get('flavor').get(key, '')
        del self.filter_properties['type'] # flavor type should't be in 'filter_properties'

        #self.filter_properties['limits'] = request.get('flavor') # ???????????????????
        self.filter_properties['force'] = request.get('policy').get('force', [])
        self.filter_properties['ignore'] = request.get('policy').get('ignore', [])
        self.filter_properties['price'] = request.get('policy').get('price', {})

        # __future__: request_spec   for multi-create etc.
        request_spec = {}

        # build_spec will be returned with cloud list scheduled in it
        build_spec = {}
        build_spec['instance_name'] = request.get('instance_name')
        build_spec['flavor'] = request.get('flavor')

        # TODO: what will be transmitted via context
        context = {}

        selected_cloud = self.filter_scheduler.select_destinations(context, request_spec, self.filter_properties)

        ########OUTPUT########OUTPUT########OUTPUT########OUTPUT##########

                                    #output#

        ########OUTPUT########OUTPUT########OUTPUT########OUTPUT##########


        cloud_list = dict(cloud_list = selected_cloud.get('name', ''))
        build_spec.update(cloud_list)
        return build_spec