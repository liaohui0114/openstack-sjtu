
from hybrid_cloud.scheduler.cloud_scheduler import filters


class DiskFilter(filters.BaseCloudFilter):

    def cloud_passes(self, cloud_state, filter_properties):

        disk_limit_gb = filter_properties['disk_gb']
        
        if cloud_state['disk_gb'] < disk_limit_gb:
            return False
        
        for host in cloud_state['hosts']:
            if host['disk_gb'] >= disk_limit_gb:
                return True
                
        return False

    @staticmethod
    def get_mark(self):
        return 'disk_gb'
    
    
