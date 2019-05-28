#! /usr/bin/env python
# -*- coding: utf8 -*-

import configparser
from fabric.api import *


#print(conf.sections())

#passwords = {}

conf = configparser.ConfigParser()
conf.read("config.ini")
data = conf.items("test1")

def tt():
    hosts = []
    passwords = {}

    for i in data:
        
        dd = i[0] + ":22"
        hosts.append(dd)
        
    return hosts
def xx():
    passwords = {}
   
    for i in data:
        dd = i[0] + ":22"

        tt = i[0] + ":22" +":" + i[1] 
        passwords[dd] = i[1]
    return passwords
hosts = tt()
passwords = xx()
env.hosts = hosts
env.passwords = passwords
def getHostName():
    run("hostname")
