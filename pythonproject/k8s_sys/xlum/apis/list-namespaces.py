#!/usr/bin/python
# -*-coding: utf-8 -*-
from __future__ import print_function
from kubernetes import config, client
from pprint import pprint
import json

'''
功能：列出所有namespace
返回值：
    成功：返回{'namespaces': [namespaces]}
    失败：返回{'namespaces': 'false'}

注意修改 config.load_kube_config 指定的kubeconfig
'''


def ListNamespaces():
    config.load_kube_config('./config')
    api_instance = client.CoreV1Api(client.ApiClient())

    namespaces = []
    result = {}

    try: 
        api_response = api_instance.list_namespace()
        for i in api_response.items:
            namespaces.append(i.metadata.name)
        result['namespaces'] = namespaces
        return json.dumps(result)
    except Exception as e:
       result['namespaces'] = 'false'
       return json.dumps(result)

