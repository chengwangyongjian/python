#!/usr/bin/python
# -*-coding: utf-8 -*-
from kubernetes import client, config
from pprint import pprint
import json


'''
功能：创建namespace
参数：
    namesapce：待创建namespace名称
返回值：
    ok：创建成功
    fales：创建失败

注意修改 config.load_kube_config 指定的kubeconfig地址
'''

def CreateNamespace(namespace, kubeconfig):
    result = {}
    config.load_kube_config(kubeconfig)

    v1 = client.CoreV1Api(client.ApiClient())
    body = client.V1Namespace()
    body.metadata = client.V1ObjectMeta(name=namespace)
    pretty = 'true'

    try:
        api_response = v1.create_namespace(body, pretty=pretty)
        result['status'] = 'ok'
        return json.dumps(result)

    except Exception as e:
        result['status'] = 'false'
        return json.dumps(result)
