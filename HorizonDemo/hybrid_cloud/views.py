from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
##added for detail.html
from hybrid_cloud.api import CloudAPI
from hybrid_cloud.api import User
####

# Create your views here.


#function: to judge if user has login;we use session
def isLogin(request):
    '''
    if request.session.get("username"):
        return True
    else:
        return False
    '''
    username = request.COOKIES.get('username') #TO GET THE COOKIES
    if username:
        print ' login'
        return True
    else:
        print 'not login'
        return False
    

def loginFunc(request):
    if isLogin(request):
        return HttpResponseRedirect("/main/")
    return render_to_response("login.html")

def mainFunc(request):
    print 'mainFunc'
    if not isLogin(request):
        return HttpResponseRedirect("/login/")
    return render_to_response("main.html")

def topFunc(request):
    return render_to_response("top.html")

def leftFunc(request):
    return render_to_response("left.html")

def indexFunc(request):
    if not isLogin(request):
        return HttpResponseRedirect("/login/")
    return render_to_response("index.html")

def overviewFunc(request):
    if not isLogin(request):
        return HttpResponseRedirect("/login/")
    return render_to_response("overview.html")

def right2Func(request):
    if not isLogin(request):
        return HttpResponseRedirect("/login/")
    return render_to_response("right2.html")

def instanceFunc(request):
    if not isLogin(request):
        return HttpResponseRedirect("/login/")
    return render_to_response("instance.html")

def instance2Func(request):
    if not isLogin(request):
        return HttpResponseRedirect("/login/")
    return render_to_response("instance2.html")

def formFunc(request):
    if not isLogin(request):
        return HttpResponseRedirect("/login/")
    return render_to_response("form.html")

####################################################################################
##for detail page
def detailFunc(request):
    if not isLogin(request):
        return HttpResponseRedirect("/login/")
    if request.method == "GET":
        print 'get method'
        serverid = request.GET.get("id")
        authurl = request.GET.get("endpoint")
        print serverid,authurl
        
        ###to get detail infos of server
        cloud = CloudAPI.CloudAPI(**User.get_nova_credentials(authurl))
        detail = cloud.getInstanceDetail(serverid)
        if detail:
            #if detail != None
            print "detail:",detail
            return render_to_response("detail.html", {"detail":detail})
    return HttpResponse("No detail Infomations")
################################################################################