from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
from django.contrib import admin
# Create your models here.

#school node:
class User(models.Model):
    username = models.CharField(max_length=50)
    #nodeIp = models.CharField(max_length=16)
    password = models.CharField(max_length=50)

  
    def __unicode__(self):
        return self.username
    
#protocol:TCP,UDP,ICMP,SNMP
class Cloud(models.Model):
    cloudname = models.CharField(max_length=50)
    endpoint = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.cloudname

#to store active_networkMeasurement informations
class CloudUser(models.Model):
    clouduser = models.CharField(max_length=50)
    cloudpassword = models.CharField(max_length=50)
    project = models.CharField(max_length=20,default="demo")
    
    user = models.ForeignKey(User,related_name="user")
    cloud = models.ForeignKey(Cloud,related_name="cloud")
    
    


    


