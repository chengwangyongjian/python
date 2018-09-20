#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Summary:
    Basic Information:
        File Name:     getconfig.py
        Author:        liyongzhe
        Bug Contact:   liyongzhe@xunlei.com
        Version:       1.0.0

    Description:
        This file is the methode to read config file and get
        argument's value from config file.

    Args:
        section: The section name of config file.
        key: The argument name under the section.
'''

import os 
import configparser

class Getconfig(object):

    def __init__(self, configpath):
        self.configpath = configpath

    def getconfig(self, section, key):
        conf = configparser.ConfigParser()
#        path = os.path.split(os.path.realpath(__file__))[0] + '/config/host.conf'
        conf.read(self.configpath)
        return conf.get(section, key)
