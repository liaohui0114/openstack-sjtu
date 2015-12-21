
from cloud_scheduler import cloud_scheduler_manager

#script, request_num = sys.argv

scheduler = cloud_scheduler_manager.CloudSchedulerManager()

requests = [

    # request 0
    {
    'flavor':{'cpu': -2, 'ram_mb': 1024, 'disk_gb': 100},
    'specific': {}
    },

    # request 1
    {

        'instance_name': 'my_instance',

        'flavor':
        {
            'type': 'small' ,
            'cpu': 4, 'ram_mb': 8192, 'disk_gb': 512,
        },

        'policy':
        {
        #    'force': ['http://192.168.1.123:5000' ],
            #'ignore': ['http://cloud_ignored_keystone'],

            'price': {'min' : 0 , 'max' : 100 },
        },

    },

    # request 2
    {

        'instance_name': 'my_instance',

        'flavor':
        {
            'type': 'small' ,
            'cpu': 1, 'ram_mb': 512, 'disk_gb': 1,
        },

        'policy':
        {
            #'force': ['http://192.168.1.123:5000' ],
            #'force': ['cloud_2'],
            #'ignore': ['http://cloud_ignored_keystone'],
            #'ignore': ['cloud_1']
            'price': {'min' : 0 , 'max' : 100 },
        },

    },

]

# static cloud_state used currently
# please go to cloud_state_manager.py
ret = scheduler.select_cloud(requests[2])
print ret

