#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/8/20
import json
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
pro_dir = os.getcwd()  #如果放在project目录，就不需要在配置绝对路径了
sys.path.append(pro_dir)
os.environ.update({"DJANGO_SETTINGS_MODULE": "xlum.settings"})

import django
django.setup()

from app01.models import NameSpace, Zone
from utils.list_namespaces import ListNamespaces
from utils.getconfig import Getconfig


def InsertSqlData(zone):
    config = Getconfig('../conf/system.conf')
    kubeconfig = config.getconfig(zone, 'kubeconfig')
    namespace_list = json.loads(ListNamespaces(kubeconfig))['namespaces']
    zone_obj = Zone.objects.filter(z_name=zone).first()
    for namespace in namespace_list:
        ns_obj = NameSpace(namespace=namespace, last_updater='admin', zone=zone_obj)
        ns_obj.save()
    print('%s的namespace已全部添加至数据库!' % zone)


def InsertAll():
    # 添加所有zone的namespace到数据库
    zone_sql = Zone.objects.values('z_name')
    for zone in zone_sql:
        InsertSqlData(zone['z_name'])


# InsertAll()
InsertSqlData('tw06m1')

