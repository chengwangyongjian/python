# -*- coding: utf-8 -*-

'''
ListPod:
    功能：获取命名空间下的pod
    参数：
        kubeconfig：kubecofnig文件位置
        namespace：指定一个namespace
    返回值：
        status：
            - ok：获取成功
            - failed：获取失败
        message：
            详细信息
        podInfo：如果status为ok，则输出pod的属性信息
'''

import json
import datetime
from dateutil.tz import tzutc
from kubernetes import client, config


def ListPod(kubeconfig, namespace):
    config.load_kube_config(kubeconfig)
    api_instance = client.CoreV1Api(client.ApiClient())

    try:
        api_response = api_instance.list_namespaced_pod(namespace)
        
        coreData = api_response.items
        replic_dict = {}
        for i in coreData:
            tmp = {}
            replic_name=i.status.container_statuses[0].name
            ctime = i.metadata.creation_timestamp
            createTime = ctime.strftime('%Y-%m-%d')
            labels = i.metadata.labels
            podName = i.metadata.name
            podKind = i.metadata.owner_references[0].kind
            podUid = i.metadata.uid
            podImage = i.spec.containers[0].image
            podNode = i.spec.node_name
            podIp = i.status.pod_ip
            tmp = {
                 'podip': podIp,'node': podNode,'uid': podUid,'image': podImage,'podkind': podKind,'labels': labels,'createtime': createTime,
            }
            if replic_name not in replic_dict.keys():
                 replic_dict[replic_name]={podName:tmp}
            else:
                 replic_dict[replic_name][podName]=tmp
        result = {'status': 'ok', 'podinfo': replic_dict}
        return json.dumps(result)
    except Exception as e:
        result = {'status': 'failed', 'message': 'get pod failed.'}
        return json.dumps(result)
