'''
Created on Nov 25, 2015

@author: stack
'''
import novaclient.client as nvclient
import cinderclient.v2.client as cdclient

def get_nova_credentials_v2(version='2',username=None,api_key=None,project_id=None,auth_url='',**kwargs):
    d = {}
    d["version"] = '2'
    d['username'] = username
    d['api_key'] = api_key
    d['project_id'] = project_id
    d['auth_url'] = auth_url
    return d

class NovaAdapter(object):
    '''
    classdocs
    '''

    def __init__(self, version='2',username=None, api_key=None, project_id=None,auth_url='',**kwargs):
        '''
        Constructor
        '''
        self.nova_client = nvclient.Client(version, username, api_key, project_id, auth_url,**kwargs)
        self.cinder_client = cdclient.Client(username, api_key, project_id, auth_url,**kwargs)
    
        
        '''
        self.credentials = get_nova_credentials_v2('2', username, api_key, project_id, auth_url)
        self.nova_client = nvclient.Client(**self.credentials)
        '''
        
    def getServerList(self):
        return self.nova_client.servers.list()
    
    def getLimits(self):
        limits = self.nova_client.limits.get().absolute
        usage_limits = {}
        for i in limits:
            #usage_limits[i.name] = i.value
            if i.name ==  "maxTotalInstances":
                usage_limits["instanceTotal"] = i.value
            elif i.name == "totalInstancesUsed":
                usage_limits["instanceUsed"] = i.value
            elif i.name == "maxTotalCores":
                usage_limits["coresTotal"] = i.value
            elif i.name == "totalCoresUsed":
                usage_limits["coresUsed"] = i.value
            elif i.name == "maxTotalRAMSize":
                usage_limits["ramTotal"] = i.value
            elif i.name == "totalRAMUsed":
                usage_limits["ramUsed"] = i.value
            elif i.name == "maxTotalFloatingIps":
                usage_limits["floatingIpsTotal"] = i.value
            elif i.name == "totalFloatingIpsUsed":
                usage_limits["floatingIpsUsed"] = i.value #always be zero??
                usage_limits["floatingIpsUsed"] = len(self.nova_client.servers.list()) #always be zero??
            '''
            name:value
            maxServerMeta:128
            maxTotalInstances:10
            maxPersonality:5
            totalServerGroupsUsed:0
            maxImageMeta:128
            maxPersonalitySize:10240
            maxTotalRAMSize:51200
            maxServerGroups:10
            maxSecurityGroupRules:20
            maxTotalKeypairs:100
            totalCoresUsed:1
            totalRAMUsed:512
            maxSecurityGroups:10
            totalFloatingIpsUsed:0
            totalInstancesUsed:1
            maxServerGroupMembers:10
            maxTotalFloatingIps:10
            totalSecurityGroupsUsed:1
            '''
            cinderlimits = self.cinder_client.limits.get().absolute
            for i in cinderlimits:
                #usage_limits[i.name] = i.value
                if i.name ==  "maxTotalVolumeGigabytes":
                    usage_limits["volumeStorage"] = i.value
                elif i.name == "totalGigabytesUsed":
                    usage_limits["totalGigabytesUsed"] = i.value
                elif i.name == "maxTotalVolumes":
                    usage_limits["volumeTotal"] = i.value
                elif i.name == "totalVolumesUsed":
                    usage_limits["volumeTotalUsed"] = i.value
            '''
            totalSnapshotsUsed:0
            maxTotalBackups:10
            maxTotalVolumeGigabytes:1000
            maxTotalSnapshots:10
            maxTotalBackupGigabytes:1000
            totalBackupGigabytesUsed:0
            maxTotalVolumes:10
            totalVolumesUsed:0
            totalBackupsUsed:0
            totalGigabytesUsed:0
            '''
        return usage_limits
    
    def getUsages(self):
        servers = self.nova_client.servers.list()
        usages = []
        #to get every server's usage
        for server in servers:
            '''
            print server.name
            print server.id
            print server.created
            print self.nova_client.flavors.get(server.flavor["id"]).ram
            print self.nova_client.flavors.find(id=server.flavor["id"]).vcpus
            print self.nova_client.flavors.get(server.flavor["id"]).disk
            '''
            usage = {}
            usage["name"] = server.name
            usage["id"] = server.id
            usage["createTime"] = server.created
            usage["ram"] = self.nova_client.flavors.get(server.flavor["id"]).ram
            usage["vcpus"] = self.nova_client.flavors.find(id=server.flavor["id"]).vcpus
            usage["disk"] = self.nova_client.flavors.get(server.flavor["id"]).disk
            
            usages.append(usage)
        
        return usages
    
    def createDefaultInstance(self,createspec):
        print('4444444');
        #image = self.nova_client.images.list()[0]    
        image = self.nova_client.images.find(name="cirros-0.3.4-x86_64-uec")
        print createspec
        flavor = self.nova_client.flavors.find(name="m1."+createspec['flavor']['type'])
        net = self.nova_client.networks.find(label='private')
        nics = [{'net-id':net.id}]
        ##create instance
        instance = self.nova_client.servers.create(name=createspec['instance_name'],image=image,flavor=flavor,nics=nics)
        return instance
    
    def createInstance(self,name,image,flavor,**kwargs):
        pass
    
    #id: instance id
    def getInstanceDetail(self,id):
        server = self.nova_client.servers.get(id)
        detail = {}
        ###server infomations
        detail["name"] = server.name
        detail["id"] = server.id
        detail["status"] = server.status
        detail["created"] = server.created
        ##flaveor informations
        #detail["id"] = server.flavor["id"]
        detail["flavor"] = self.nova_client.flavors.get(server.flavor["id"]).name
        detail["ram"] = self.nova_client.flavors.get(server.flavor["id"]).ram
        detail["vcpus"] = self.nova_client.flavors.find(id=server.flavor["id"]).vcpus
        detail["disk"] = self.nova_client.flavors.get(server.flavor["id"]).disk
        ##addr informations
        addresses = []
        address = server.addresses["private"]
        '''
        for addr in address:
            print addr["OS-EXT-IPS:type"],addr["addr"]
        '''
        for addr in address:
            addresses.append(addr["addr"]) #get ipv4,ipv6,floating ip
        
        detail["address"] = addresses
        detail["image"] = self.nova_client.images.get(server.image['id']).name
        power_states = [
        'NOSTATE',      # 0x00
        'Running',      # 0x01
        '',             # 0x02
        'Paused',       # 0x03
        'Shutdown',     # 0x04
        '',             # 0x05
        'Crashed',      # 0x06
        'Suspended'     # 0x07
        ]
        detail["power_state"] = power_states[getattr(server, "OS-EXT-STS:power_state")]
        detail["availability_zone"] = getattr(server, "OS-EXT-AZ:availability_zone")
        #########end#########33
        return detail
        
        
