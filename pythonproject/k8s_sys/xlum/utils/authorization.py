#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
ListClusterRoles:
    功能：获取所有clusterroles
    参数：
        kubeconfig：集群kubeconfig文件路径
        username：用户名
        clusterrole：权限
        namespace：命名空间
        zone：集群名称
    返回：
        正常：{'clusterroles': [clusterroles]}
        失败：{'clusterroles': 'failed'}
    注意修改config文件路径

ClusterRoleBinding:
    功能：用户绑定默认clusterrole
    返回：
        正常：{'status': 'ok', 'message': 'binding role ok.'}
        失败：{'status': 'failed', 'message': 'binding role failed.'}
        binding已存在：{'status': 'failed', 'message': 'rolebinding already exists.'}
        参数错误：{'status': 'failed', 'message': 'wrong clusterrole type'}
    参数：
        - username：用户名
        - clusterrole：需要什么样的权限（superadmin > admin > edit > viewer）
        - namespace：命名空间
'''
from __future__ import print_function

import json
import subprocess
from kubernetes import client, config


def ClusterRoleBinding(username, clusterrole, namespace, kubeconfig, zone):
    result = {}

    if clusterrole == 'superadmin':
        role = 'cluster-admin'
    elif clusterrole == 'admin':
        role = 'admin'
    elif clusterrole == 'editer':
        role = 'edit'
    elif clusterrole == 'viewer':
        role = 'view'
    else:
        result = {'status': 'failed', 'message': 'wrong clusterrole type'}
        return json.dumps(result)

    try:

        cmdBindRole = 'kubectl %s create rolebinding %s-cluster-admin-binding --clusterrole=%s --user=%s --namespace=%s --kubeconfig=%s > /dev/null 2>&1' % (
        zone, username, role, username, namespace, kubeconfig)
        cmdSend = subprocess.Popen(cmdBindRole, shell=True)
        code = cmdSend.wait()

        if code == 0:
            result = {'status': 'ok', 'message': 'binding role ok.'}
            return json.dumps(result)
        else:
            result = {'status': 'failed', 'message': 'rolebinding already exists.'}
            return json.dumps(result)

    except Exception as e:
        result = {'status': 'failed', 'message': 'binding role failed.'}
        return json.dumps(result)


def ListClusterRoles(kubeconfig):
    result = {}
    clusterRoles = []
    config.load_kube_config(config_file=kubeconfig)

    try:
        api_instance = client.RbacAuthorizationV1Api(client.ApiClient())
        api_response = api_instance.list_cluster_role()
        for i in api_response.items:
            clusterRoles.append(i.metadata.name)
        result['clusterroles'] = clusterRoles
        return json.dumps(result)

    except Exception as e:
        result['clusterroles'] = 'failed'
        return json.dumps(result)
