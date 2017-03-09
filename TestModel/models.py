from __future__ import unicode_literals
from testdj.settings import DB_NAME
# from mongoengine import *
from django.db import models

class Test(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    age = models.CharField(default='', max_length=100)
    type = models.CharField(default='friendly', max_length=100)

    # class Meta:
    #     ordering = ('created',)