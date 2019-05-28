#! /usr/bin/env python
# -*- coding: utf8 -*-

from fabric.api import *


env.user = "root"
env.password = "root"
env.hosts = ["xxx"]

def getHostName():
    run("hostname")