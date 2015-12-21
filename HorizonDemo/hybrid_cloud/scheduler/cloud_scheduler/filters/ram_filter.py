
from hybrid_cloud.scheduler.cloud_scheduler import filters


class RamFilter(filters.BaseCloudFilter):

    def cloud_passes(self, cloud_state, filter_properties):
        ram_limit_mb = filter_properties['ram_mb']

        if cloud_state['ram_mb'] >= ram_limit_mb:
            for host in cloud_state['hosts']:
                if host['ram_mb'] >= ram_limit_mb:
                    return True

        return False


    @staticmethod
    def get_mark(self):
        return 'ram_mb'
  