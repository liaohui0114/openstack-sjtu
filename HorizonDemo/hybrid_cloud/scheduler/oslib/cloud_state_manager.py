
from hybrid_cloud.scheduler.oslib.get_data import *
class CloudState(object):
    """This class is incomplete
    __future__
    1. data structure of cloud state
    2. update cloud state data from openstack nova

    -- yufei 2015-12-11 15:44:20
    """

    def __init__(self, cloud, compute):
        # cloud - name/keystone url of the cloud
        # compute - where it update data from



        # TODO: remove this when finishing this method
        raise Exception('This class is incomplete!')

    def update_from_cloud(self, cloud):
        raise Exception('This class is incomplete!')


class CloudStateManager(object):

    def get_all_cloud_states(self):


        cloud_states_list = []
        url_list = ['192.168.1.123:5000','192.168.1.125:5000']

        for i in url_list:
            raw_data = get_data(i)

            key_name = 'name'
            #val_name = 'cloud_1'

            # address of keystone as the name of
            val_name = i

            key_cpu = 'cpu'
            val_cpu = get_total_cpu(raw_data)

            key_ram_mb = 'ram_mb'
            val_ram_mb = get_total_ram_mb(raw_data)

            key_disk_gb = 'disk_gb'
            val_disk_gb = get_total_disk_gb(raw_data)

            key_hosts = 'hosts'
            val_hosts = get_host_info(raw_data)

            cloud_states_list.append({key_name:val_name,key_cpu:val_cpu,key_ram_mb:val_ram_mb,key_disk_gb:val_disk_gb,key_hosts:val_hosts})
            print ('1111111111111111111111111111111')

        return cloud_states_list




    # def get_all_cloud_states(self):
    #
    #     return [
    #
    #         # cloud 1
    #         {
    #             'name': 'cloud_1',
    #             'cpu': 20,
    #             'ram_mb': 63488,
    #             'disk_gb': 7020,
    #             'price': 10,
    #             'hosts':[
    #                 {'name': 'host_0', 'cpu': 2, 'ram_mb': 1024, 'disk_gb': 20},
    #             ],
    #         },
    #
    #         # cloud 2
    #         {
    #             'name': 'cloud_2',
    #             'cpu': 10,
    #             'ram_mb': 10000,
    #             'disk_gb': 7020,
    #             'price':-200,
    #             'hosts':[
    #                 {'name': 'host_0', 'cpu': 2, 'ram_mb': 1024, 'disk_gb': 20},
    #             ],
    #         },
    #
    #         # cloud 3
    #         {
    #             'name': 'cloud_3',
    #             'cpu': 10000,
    #             'ram_mb': 1000000,
    #             'disk_gb': 111110,
    #             'price': 10,
    #             'hosts':[
    #                 {'name': 'host_0', 'cpu': 2, 'ram_mb': 1024, 'disk_gb': 20},
    #             ],
    #         },

    #    ]