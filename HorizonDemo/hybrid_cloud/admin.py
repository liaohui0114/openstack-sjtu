# -*- conding:utf-8 -*-
from django.contrib import admin

# Register your models here.

from django.contrib import admin

from models import User,Cloud,CloudUser
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password')
    
admin.site.register(User,UserAdmin) #register SchoolNode

class CloudAdmin(admin.ModelAdmin):
    list_display = ('id','cloudname','endpoint')

admin.site.register(Cloud,CloudAdmin)

class CloudUserAdmin(admin.ModelAdmin):
    list_display = ('id','clouduser','cloudpassword','project','user','cloud')
    
admin.site.register(CloudUser,CloudUserAdmin)