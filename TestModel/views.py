#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
import time
import MySQLdb
import MySQLdb.cursors
import mysql.connector
from django.shortcuts import render_to_response
from django.http import *
from models import Test
import pymongo
import logging
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from TestModel.serializers import UserSerializer, GroupSerializer, TestSerializer
from rest_framework import permissions

# 这两个模块把序列化后的数据包装成 api
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


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
# @permission_classes((permissions.AllowAny,))
def get_detail(request, *args):
    '''获取用户详情'''
    cnn = mysql.connector.connect(user='root', password='199284', database='django_test', host='127.0.0.1', port=3306, buffered=True)
    cursor = cnn.cursor()
    sql = "select * from testmodel_test where {0} = {1}".format(args[0], args[1])
    cursor.execute(sql)
    cnn.commit()

    print sql

    index = cursor.description
    result = []
    for res in cursor.fetchall():
        row = {}
        for i in range(len(index) - 1):
            row[index[i][0]] = res[i]
        result.append(row)

    # print result
    # print json.dumps(result)

    if request.method == 'GET':
        # list = Test.objects.all()
        # print list
        # serializer = TestSerializer(list, many=True)
        # print serializer.data
        # return Response(serializer.data)

        # data = {"name": args[0]}
        # serializer = TestSerializer(cursor.fetchall(), many=True)
        # data = serializer.data
        # data['sql'] = sql
        # print data

        return HttpResponse(json.dumps(result, ensure_ascii=False))
    elif request.method == 'POST':
        print 'post'

    cursor.close()
    cnn.close()

@api_view(['GET', 'POST'])
# @permission_classes((permissions.AllowAny,))
def add_user(request, **kw):
    '''添加用户'''
    cnn = mysql.connector.connect(user='root', password='199284', database='django_test', host='127.0.0.1', port=3306)
    # if request.method == 'POST':
        # serializer = TestSerializer(list, many=True)
    # for key,value in kw.iteritems():
    #     print key, value

    # for key,value in request.data:
    # print request.data['description']

    cursor = cnn.cursor()
    sql = "insert into testmodel_test (name, age, type) values('{0}', '{1}', '{2}')".format(
        request.data['name'], request.data['age'], request.data['type']
    )
    result = cursor.execute(sql)

    cnn.commit()
    cursor.close()
    cnn.close()

    return Response({"status": result})