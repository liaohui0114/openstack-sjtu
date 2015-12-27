from CloudAPI import *
import novaclient.client as nvclient
import cinderclient.v2.client as cdclient
import time
AUTHURL = "http://192.168.1.164:5000/v2.0"
USER = "admin"
PASSWD = "admin"
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
    try:
        nc = CloudAPI(**get_nova_credentials_v2())
        if nc.isSchedulable():
            limits = nc.getLimits()
            if limits:
                for key in limits:
                    print key
            else:
                print 'return None'
            
            usage =  nc.getUsages()
            print usage
            for u in usage:
                print nc.getInstanceDetail(u["id"])

            servers = nc.getAuth().getServerList()
            id = ''
            for server in servers:
                print server.id
                id = server.id
            #print nc.getInstanceDetailAll()
                
            #create instance
            #nc.createInstance('lh_vm1')
            
            nova = nvclient.Client('2',**get_nova_credentials_v2())
            print nova.floating_ips.list()
            #server = nova.servers.get(id)
            #print server.status #SHUTOFF,ACTIVE
            #server.delete() #teminate
            flag = True
            if flag:
                print 'yes'
            #floatingip = nova.floating_ips.create()
            #if floatingip:
                #print floatingip
                #server = nova.servers.get(id)
                #server.remove_floating_ip("192.168.1.111")
                #server.add_floating_ip(floatingip)
                
                #server.stop() #stop
                #time.sleep(5000)
                #server.start() #start
                #server.remove_floating_ip("192.168.1.101")
    
        
    except Exception,e:
        print Exception,":",e
 