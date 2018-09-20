#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import subprocess

'''
功能：创建kubeconfig
参数：
    apiserver：apiserver地址
    capath：ca证书地址
    username：用户名
    zone：集群名称
返回值：
    status：
        - ok：创建成功
        - failed：创建失败
'''


def CreateKubeconfig(apiserver, capath, username, zone):
    userZoneDir = '/home/%s/%s' % (username, zone)
    result = {'username': username, 'apiserver': apiserver, 'kubeconfig': {}}
    try:
        kubeconfigPath = '%s/%s.kubeconfig' % (userZoneDir, username)
        crtPath = '%s/%s.crt' % (userZoneDir, username)
        keyPath = '%s/%s.key' % (userZoneDir, username)

        cmdSetCluster = 'kubectl %s config set-cluster kubernetes --server=https://%s:6443 --certificate-authority=%s --embed-certs=true --kubeconfig=%s > /dev/null 2>&1' % (zone, apiserver, capath, kubeconfigPath)
        cmdSend = subprocess.Popen(cmdSetCluster, shell=True)
        cmdSend.wait()

        cmdSetKey = 'kubectl %s config set-credentials %s --client-certificate=%s --client-key=%s --embed-certs=true --kubeconfig=%s > /dev/null 2>&1' % (zone, username, crtPath, keyPath, kubeconfigPath)
        cmdSend = subprocess.Popen(cmdSetKey, shell=True)
        cmdSend.wait()

        cmdSetContext = 'kubectl %s config set-context %s-context --cluster=kubernetes --user=%s --kubeconfig=%s > /dev/null 2>&1' % (zone, username, username, kubeconfigPath)
        cmdSend = subprocess.Popen(cmdSetContext, shell=True)
        cmdSend.wait()

        cmdUseContext = 'kubectl %s config use-context %s-context --kubeconfig=%s > /dev/null 2>&1' % (zone, username, kubeconfigPath)
        cmdSend = subprocess.Popen(cmdUseContext, shell=True)
        cmdSend.wait()

        result['kubeconfig']['configfile'] = kubeconfigPath
        result['kubeconfig']['status'] = 'ok'

        cmdChangeOwner = 'chown -R %s:%s %s' % (username, username, userZoneDir)
        cmdSend = subprocess.Popen(cmdChangeOwner, shell=True)
        cmdSend.wait()

        return json.dumps(result)

    except Exception as e:
        result['kubeconfig']['configfile'] = kubeconfigPath
        result['kubeconfig']['status'] = 'failed'
        return json.dumps(result)
