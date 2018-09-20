#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
功能： 创建用户证书
参数：
    zone：集群名称
    username：用户名
    group：组名
    apiserver：apiserver地址
    certday：证书有效期
    capath：ca证书地址
    cakeypath：ca私钥地址
返回值：
    status:
        - ok：创建成功
        - failed：创建失败
'''

import os
import json
import subprocess


def CreateCerts(username, apiserver, certday, capath, cakeypath, zone):
    result = {'zone': zone, 'username': username, 'group': username, 'apiserver': apiserver, 'certs': {}}
    try:
        userZoneDir = '/home/%s/%s' % (username, zone)
        if not os.path.isdir(userZoneDir):
            cmdCreateDir = 'mkdir %s' % userZoneDir
            cmdSend = subprocess.Popen(cmdCreateDir, shell=True)
            cmdSend.wait()

        userKey = '%s/%s.key' % (userZoneDir, username)
        cmdKey = 'openssl genrsa -out %s 2048 > /dev/null 2>&1' % userKey
        cmdSend = subprocess.Popen(cmdKey, shell=True)
        cmdSend.wait()
        result['certs']['pubkey'] = {'path': userKey, 'status': 'ok'}

        userCsr = '%s/%s.csr' % (userZoneDir, username)
        cmdCert = 'openssl req -new -key %s -out %s -subj "/CN=%s/O=%s" > /dev/null 2>&1' % (
        userKey, userCsr, username, username)
        cmdSend = subprocess.Popen(cmdCert, shell=True)
        cmdSend.wait()
        result['certs']['csr'] = {'path': userCsr, 'status': 'ok'}

        userCrt = '%s/%s.crt' % (userZoneDir, username)
        cmdSign = 'openssl x509 -req -in %s -CA %s -CAkey %s -CAcreateserial -out %s -days %s > /dev/null 2>&1' % (
        userCsr, capath, cakeypath, userCrt, certday)
        cmdSend = subprocess.Popen(cmdSign, shell=True)
        cmdSend.wait()
        result['certs']['crt'] = {'path': userCrt, 'status': 'ok'}
        result['certs']['status'] = 'ok'

        cmdChangeOwner = 'chown -R %s:%s %s' % (username, username, userZoneDir)
        cmdSend = subprocess.Popen(cmdChangeOwner, shell=True)
        cmdSend.wait()

        return json.dumps(result)
    except Exception as e:
        result['certs']['status'] = 'failed'
        return json.dumps(result)
