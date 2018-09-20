# -*- coding: utf-8 -*-

'''
DeleteUser:
  功能： 删除系统用户并解除权限绑定
  参数：
    username：用户名
    nslist：用户已绑定namespace列表
    kubeconfig：集群kubeconfig文件路径
    zone：集群名称
  返回值：
  	status：返回状态
  		- ok：成功
  		- failed：失败
  	message：返回信息
  	namespacelist：在解绑权限时如果有部分namespace解绑失败则返回这些失败namespaces的列表

'''

import json
import subprocess

def DeleteUser(username, nslist, kubeconfig, zone):
    try:
        cmdDeleteSystemUser = 'userdel -r %s' % username
        cmdSend = subprocess.Popen(cmdDeleteSystemUser, shell=True)
        cmdSend.wait()
    except Exception as e:
        result = {'status': 'failed', 'message': 'delete system-user failed'}
        return json.dumps(result)

    success = []
    fail = []
    for namespace in nslist:
        try:
            cmdUnbind = 'kubectl %s delete rolebinding %s-cluster-admin-binding -n %s --kubeconfig=%s' % (zone, username, namespace, kubeconfig)
            cmdSend = subprocess.Popen(cmdUnbind, shell=True)
            cmdSend.wait()
            success.append(namespace)
        except Exception as e:
            fail.append(namespace)
            continue

    if len(fail) == 0:
        result = {'status': 'ok', 'message': 'delete user success.'}
        return json.dumps(result)
    else:
        result = {'status': 'failed', 'message': 'unbinding failed.', 'namespacelist': fail}
        return json.dumps(result)
