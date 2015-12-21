from hybrid_cloud.scheduler.cloud_scheduler import filters


class CPUFilter(filters.BaseCloudFilter):

    def cloud_passes(self, cloud_state, filter_properties):
        cpu_limit = filter_properties['cpu']
        
        if cloud_state['cpu'] < cpu_limit:
            return False
        
        for host in cloud_state['hosts']:
            if host['cpu'] >= cpu_limit:
                return True
                
        return False

    @staticmethod
    def get_mark(self):
        return 'cpu'