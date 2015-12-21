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
        if username == "admin" and password == "admin":
            
            #return HttpResponseRedirect("/main/")
            response = HttpResponse(json.dumps({}), content_type="application/json")
            
            #createSession(response,username)
            #response.session["username"] = username
            response.set_cookie('username', username, 3600) #create cookies
            return response

def logoutAction(request):
    print 'logoutAction'
    username = request.COOKIES.get('username') #TO GET THE COOKIES
    if username:
        response = HttpResponseRedirect("/main/")
        response.delete_cookie('username')
        return response

def overviewAction(request):
    print 'overviewAction'
    if request.method == 'POST':
        authurl = request.POST["url"]
        print authurl
        cloud = CloudAPI.CloudAPI(**User.get_nova_credentials(authurl))
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
        authurl = request.POST["url"]
        print authurl
        cloud = CloudAPI.CloudAPI(**User.get_nova_credentials(authurl))
        if cloud.isSchedulable():
            details = cloud.getInstanceDetailAll()
        if details:
            print details
            return HttpResponse(json.dumps({"details":details}), content_type="application/json")
