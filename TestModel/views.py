#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time
from django.shortcuts import render_to_response
from django.http import *
from models import Test
import pymongo
import logging
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from TestModel.serializers import UserSerializer, GroupSerializer, TestSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

def index(request):
    entry = Test(name='lidong')
    entry.phone = '13410320008'
    logging.debug('**************')

    # entry.save()
    # resp = "hello %s , phone :%s" %(entry.name, entry.phone)
    # return HttpResponse(resp)
    return HttpResponse('zhangtan')

def showStudents(request):
     list = [{'id': 1, 'name': 'Jack'}, {'id': 2, 'name': 'Rose'}]
     return render_to_response('student.html', {'students': list})

def show_mongo(request):
    conn = pymongo.MongoClient('118.123.173.86', 27017)
    try:
        conn.database_names()
    except:
        conn['mianbaoquan'].authenticate('mbq_dbOwner', 'mbq@2016')

    db = conn['mianbaoquan']
    coll = db['position']

    num = coll.count()
    return render_to_response('base.html', {'nums': num})

class UserViewSet(viewsets.ModelViewSet):
    """
    查看、编辑用户的界面
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    查看、编辑组的界面
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['GET', 'POST'])
def get_detail(request, *args):
    '''获取用户详情'''
    if request.method == 'GET':
        list = Test.objects.all()
        serializer = TestSerializer(list, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print 'post'

# def get
