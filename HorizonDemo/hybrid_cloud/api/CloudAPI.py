'''
Created on Nov 26, 2015

@author: stack
'''
from __future__ import division
import NovaAdapter


class CloudAPI(object):
    '''
    classdocs
    '''


    def __init__(self, username=None,api_key=None,project_id=None,auth_url='',**kwargs):
        '''
        Constructor
        '''
        self.username = username
        self.api_key = api_key
        self.project_id = project_id
        self.auth_url = auth_url
        self.kwargs = kwargs
        self.authClient = None
    
    #with guang yang
    def isSchedulable(self):
        ##do scheduling here
        return True
    
    
    #to get authorize
    def getAuth(self):
        try:
            if not self.authClient:
                client = NovaAdapter.NovaAdapter(username=self.username,
                                                 api_key = self.api_key,
                                                 project_id = self.project_id,
                                                 auth_url = self.auth_url,
                                                 **self.kwargs)
                self.authClient = client  ##initialize self.authClient when first call getAuth
            else:
                client = self.authClient 
            return client
        except Exception,e:
            print Exception,":",e
            return False # if failed,return False
        
    def createInstance(self,name,image='',flavor='',**kwargs):
        try:
            client = self.getAuth()
            # if client not None
            if client:
                client.createDefaultInstance(name) #you can use createInstance either
        except Exception,e:
            print Exception,":",e
            return False # if failed,return False
        
        return True
    
    def getLimits(self):
        tmp_lists = []
        lists=[]
        try:
            client = self.getAuth()
            if client:
                limits = client.getLimits()
                '''for i,j in limits.items():
                    tmpList=[]
                    tmpList.append(i)
                    tmpList.append(j)
                    lists.append(tmpList)'''
                p=limits["instanceUsed"]/limits["instanceTotal"]
                tmp_lists.append(['Used',p*100])
                tmp_lists.append(['NotUsed',(1-p)*100])
                lists.append(tmp_lists)
                tmp_lists = []
                p=limits["coresUsed"]/limits["coresTotal"]
                tmp_lists.append(['Used',p*100])
                tmp_lists.append(['NotUsed',(1-p)*100])
                lists.append(tmp_lists)
                tmp_lists = []
                p=limits["ramUsed"]/limits["ramTotal"]
                tmp_lists.append(['Used',p*100])
                tmp_lists.append(['NotUsed',(1-p)*100])
                lists.append(tmp_lists)
                tmp_lists = []
                p=limits["floatingIpsUsed"]/limits["floatingIpsTotal"]
                tmp_lists.append(['Used',p*100])
                tmp_lists.append(['NotUsed',(1-p)*100])
                lists.append(tmp_lists)
                tmp_lists = []
                p=limits["totalGigabytesUsed"]/limits["volumeStorage"]
                tmp_lists.append(['Used',p*100])
                tmp_lists.append(['NotUsed',(1-p)*100])
                lists.append(tmp_lists)


        except Exception,e:
            print Exception,":",e
            return None # if failed,return None
        
        return lists
    
    def getUsages(self):
        try:
            client = self.getAuth()
            if client:
                usages = client.getUsages()
        except Exception,e:
            print Exception,":",e
            return None # if failed,return None
        
        return usages
    
    def getInstanceDetail(self,id=''):
        try:
            client = self.getAuth()
            if client:
                detail = client.getInstanceDetail(id)
        except Exception,e:
            print Exception,":",e
            return None # if failed,return None
        
        return detail

    def getInstanceDetailAll(self):
    	try:
    		client = self.getAuth()
    		if client:
    			details = []
    			servers = client.getServerList()
    			for server in servers:
    				details.append(client.getInstanceDetail(server.id))
    	except Exception,e:
            print Exception,":",e
            return None # if failed,return None
        
        return details
