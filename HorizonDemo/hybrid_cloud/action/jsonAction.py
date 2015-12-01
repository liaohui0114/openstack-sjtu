'''
Created on Nov 20, 2015

@author: liaohui
'''
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
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
        if username == "admin" and password == "1":
            
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
    print 'createInstanceAction'
    if request.method == 'POST':
        name = request.POST.get('name')
        print name
        cloud = CloudAPI.CloudAPI(**User.get_nova_credentials())
        if cloud.isSchedulable():
            result = cloud.createInstance(name)
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
