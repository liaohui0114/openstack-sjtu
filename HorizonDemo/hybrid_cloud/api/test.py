from CloudAPI import *
AUTHURL = "http://192.168.1.157:5000/v2.0"
USER = "admin"
PASSWD = "1"
TENANT="demo"
REGION = "RegionOne"

NOVA_VER = "2"

def get_nova_credentials_v2():
    d = {}
    #d["version"] = '2'
    d['username'] = USER
    d['api_key'] = PASSWD
    d['auth_url'] = AUTHURL
    d['project_id'] = TENANT
    return d

if __name__ == "__main__":
    """
    try:
        nc = NovaAdapter(**get_nova_credentials_v2())
        servers =  nc.getServerList()
        for s in servers:
            print s.id
        usages = nc.getLimits()
        for key,value in usages.items():
            print key,value
        
        print nc.getUsages()
        '''
        ##create instance
        instance = nc.createDefaultInstance("liaohui_vm2")
        print instance.id
        print nc.getUsages()
        '''
        print nc.getInstanceDetail(servers[0])
    except Exception,e:
        print Exception,":",e
    """
    try:
        nc = CloudAPI(**get_nova_credentials_v2())
        if nc.isSchedulable():
            limits = nc.getLimits()
            if limits:
                for key,value in limits.items():
                    print key,value
            else:
                print 'return None'
            
            usage =  nc.getUsages()
            print usage
            for u in usage:
                print nc.getInstanceDetail(u["id"])
                
            #create instance
            #nc.createInstance('lh_vm1')
        
    except Exception,e:
        print Exception,":",e