from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import hybrid_cloud.action.jsonAction


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HorizonDemo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    
    ############for views###################
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','hybrid_cloud.views.loginFunc'),
    url(r'^login/$','hybrid_cloud.views.loginFunc'),
    url(r'^main/$','hybrid_cloud.views.mainFunc'),
    url(r'^top/$','hybrid_cloud.views.topFunc'),
    url(r'^left/$','hybrid_cloud.views.leftFunc'),
    url(r'^index/$','hybrid_cloud.views.indexFunc'),
    url(r'^right1/$','hybrid_cloud.views.right1Func'),
    url(r'^right2/$','hybrid_cloud.views.right2Func'),
    url(r'^instance1/$','hybrid_cloud.views.instance1Func'),
    url(r'^instance2/$','hybrid_cloud.views.instance2Func'),
    url(r'^form/$','hybrid_cloud.views.formFunc'),
    url(r'^detail/$','hybrid_cloud.views.detailFunc'),
    
    ##############for Action###########################
    url(r'action/loginAction','hybrid_cloud.action.jsonAction.loginAction'),
    url(r'action/logoutAction','hybrid_cloud.action.jsonAction.logoutAction'),
    url(r'action/overviewAction','hybrid_cloud.action.jsonAction.overviewAction'),
    url(r'action/createInstanceAction', 'hybrid_cloud.action.jsonAction.createInstanceAction'),
    url(r'action/instanceDetailAction', 'hybrid_cloud.action.jsonAction.instanceDetailAction'),
    ############for static files##########################
    url(r'static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),#liao,for static files like js,css,jpeg
    
)

urlpatterns += staticfiles_urlpatterns()