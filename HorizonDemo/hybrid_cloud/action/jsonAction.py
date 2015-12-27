'''
Created on Nov 20, 2015

@author: liaohui
'''
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from hybrid_cloud.scheduler.cloud_scheduler import cloud_scheduler_manager
import json
from hybrid_cloud.api import CloudAPI
from hybrid_cloud.api import User
import hybrid_cloud.models as db

def get_nova_credentials(request,cloudname):
    d = {}
    cloudinfo = request.session.get("cloud")
    if cloudinfo and cloudinfo.has_key(cloudname):
        d['username'] = cloudinfo[cloudname]["user"]
        d['api_key'] = cloudinfo[cloudname]["pwd"]
        d['auth_url'] = cloudinfo[cloudname]["endpoint"]
        d['project_id'] = cloudinfo[cloudname]["project"]
    
    return d



def loginAction(request):
    print 'loginAction'
    '''
    if request.method == "GET":
        print 'get method'
        username = request.GET.get("username")
        password = request.GET.get("password")
        print username,password
        if username == "liaohui" and password == "liaohui":
            print 'success'
            return HttpResponseRedirect("/main/")
    '''
    if request.method == "POST":
        print 'post method'
        #get username pwd from post method
        username = request.POST["username"]
        password = request.POST["password"]
        print username,password
        
        #if username == "admin" and password == "admin":
        #db operation
        if db.User.objects.get(username=username,password=password):    
            #return HttpResponseRedirect("/main/")
            response = HttpResponse(json.dumps({}), content_type="application/json")
            
            
            #query db
            userinfo = db.User.objects.get(username=username,password=password)
            usercloudinfo = db.CloudUser.objects.filter(user=userinfo)
    
            #print usercloudinfo,usercloudinfo[0].id,usercloudinfo[0].clouduser,usercloudinfo[0].cloudpassword,usercloudinfo[0].cloud.cloudname,usercloudinfo[0].cloud.endpoint
            cloudinfo = {}
            for item in usercloudinfo:
                u = item.clouduser
                pwd = item.cloudpassword
                project = item.project
                cloudname = item.cloud.cloudname
                cloudendpoint = item.cloud.endpoint
                cloudinfo[cloudname] = {"user":u,"pwd":pwd,"project":project,"endpoint":cloudendpoint}
            #request.session["cloud"] = {"cloud1":{"user":"liaohui","pwd":"liaohui","endpoint":"https://192.168.1.1"},"cloud2":{"user":"yangguang","pwd":"yangguang","endpoint":"https://192.168.1.1"}}
            ###################################################################
            #create session
            request.session["cloud"] = cloudinfo
            #create cookies
            response.set_cookie('username', username, 3600) #create cookies
            #################################################################
            
            print 'session info:',request.session.get("cloud") #print for test
            #get_nova_credentials(request,"cloud1") #for test
            
            return response

def logoutAction(request):
    print 'logoutAction'
    username = request.COOKIES.get('username') #TO GET THE COOKIES
    if username:
        response = HttpResponseRedirect("/main/")
        response.delete_cookie('username')
        return response
    if request.session.get('cloud'):
        del request.session['cloud']
            

def overviewAction(request):
    print 'overviewAction'
    if request.method == 'POST':
        authurl = request.POST["url"]
        cloudname = request.POST["cloud"]
        print authurl
        print cloudname
        #cloud = CloudAPI.CloudAPI(**User.get_nova_credentials(authurl))
        cloud = CloudAPI.CloudAPI(**get_nova_credentials(request,cloudname))
        if cloud.isSchedulable():
            ##to judge if cloud can be schedulable
            limits = cloud.getLimits()
            usages = cloud.getUsages()
        
        #if limits != None and usages != None
        if limits and usages:
            print limits,usages
            return HttpResponse(json.dumps({"limits":limits,"usages":usages}), content_type="application/json")
        
        ##esle operation failed

def createInstanceAction(request):
    scheduler = cloud_scheduler_manager.CloudSchedulerManager()
    instancetype={
        'tiny':{'type':'tiny','cpu': 1, 'ram_mb': 512, 'disk_gb': 1},
        'small':{'type':'small','cpu': 1, 'ram_mb': 2048, 'disk_gb': 20},
        'medium':{'type':'medium','cpu': 2, 'ram_mb': 4096, 'disk_gb': 40},
        'large':{'large':'small','cpu': 4, 'ram_mb': 8192, 'disk_gb': 80},
        'xlarge':{'xlarge':'small','cpu': 8, 'ram_mb': 16384, 'disk_gb': 160}
    }
    print 'createInstanceAction'
    if request.method == 'POST':
        name = request.POST.get('name')
        instance_type = request.POST.get('type')
        print instance_type
        request={
            'instance_name':name,
            'flavor':instancetype[instance_type],
            'policy':{

            }
        }
        create_spec=scheduler.select_cloud(request);
        print create_spec
        cloud = CloudAPI.CloudAPI(**User.get_nova_credentials("http://"+create_spec['cloud_list']+"/v2.0"))
        if cloud.isSchedulable():
            result = cloud.createInstance(create_spec)
            print result
    return HttpResponse("finished")

def instanceDetailAction(request):
    print 'instanceDetailAction'
    if request.method == 'POST':
        #authurl = request.POST["url"]
        cloudname = request.POST["cloud"]
        cloud = CloudAPI.CloudAPI(**get_nova_credentials(request,cloudname))
        if cloud.isSchedulable():
            details = cloud.getInstanceDetailAll()
        if details:
            print "detailsssssss",details
            return HttpResponse(json.dumps({"details":details}), content_type="application/json")
        
def instanceActionsAction(request):
    print 'instacneActionsAction'
    if request.method == 'POST':
        actions = request.POST["actions"]
        cloudname = request.POST["cloud"]
        serverid = request.POST["serverid"]
        print actions,cloudname,serverid
        cloud = CloudAPI.CloudAPI(**get_nova_credentials(request,cloudname))
        flag = False # to judge if the action was successed
        if actions:
            if "start" == actions:
                flag = cloud.startServer(serverid)
            elif "stop" == actions:
                flag = cloud.stopServer(serverid)
            elif "terminate" == actions:
                flag = cloud.terminateServer(serverid)
            elif "addfloatingip" == actions:
                flag = cloud.addFloatingIps(serverid)
        if flag:       
            return HttpResponse(json.dumps({}), content_type="application/json")   
