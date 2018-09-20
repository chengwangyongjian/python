#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import random
import string
import subprocess

'''
功能： 创建系统用户，先判断用户是否存在，不存在则创建用户并生成密码。
参数：
    username：用户名
返回值：
    username：用户名
    password：随机密码(13位)
    status：返回状态
       - ok：创建成功或用户已存在
       - failed: 创建失败
    message: 返回信息
'''


def CreateSystemUser(username):
    result = {}
    passLength = 13
    cmdSearch = 'id %s 2> /dev/null' % (username)
    user = os.popen(cmdSearch).read().strip()

    if not user:
        try:
            cmdCreate = 'useradd %s' % (username)
            cmdSend = subprocess.Popen(cmdCreate, shell=True)
            cmdSend.wait()
            result['username'] = username

            chars = string.ascii_letters + string.digits
            password = ''.join(random.sample(chars, passLength))
            cmdChangePass = 'echo "%s:%s" | chpasswd' % (username, password)
            cmdSend = subprocess.Popen(cmdChangePass, shell=True)
            cmdSend.wait()
            result['password'] = password
            result['status'] = 'ok'
            result['message'] = 'create user success.'
            return json.dumps(result)

        except Exception as e:
            result['username'] = username
            result['status'] = 'failed'
            result['message'] = 'create user failed.'
    else:
        result['username'] = username
        result['status'] = 'ok'
        result['message'] = 'user already exists.'
        return json.dumps(result)
