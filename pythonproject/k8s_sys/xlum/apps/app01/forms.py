#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/8/23

from django import forms

from .models import User, Group

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=2, label='用户名', required=True,
                               error_messages={
                                   "min_length": '最小长度为2个字符',
                                   "max_length": '最大长度为100个字符',
                                   "required": '必填'
                               })
    expire_time = forms.IntegerField(required=True, label='证书失效时间')
    if_create_ns = forms.CharField(required=True, label='是否创建同名namespace')
    # clusterrole = forms.IntegerField(required=True, error_messages={"required": '必填'})
    # namespace = forms.CharField(required=True, error_messages={"required": '必填'})
