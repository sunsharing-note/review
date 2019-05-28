#! /usr/bin/env python
# -*- coding: utf8 -*-

from fabric.api import *
import datetime


env.user = "root"
env.password = "root"
env.hosts = ["root@127.0.0.1"]

def getHostName():
    run("hostname")

def deploy():
    remote_dir = "/data/tomcat/"
    tomcat_name = "apache-tomcat-8.0.45.tar.gz"
    start_dir = "/data/tomcat/apache-tomcat-8.0.45/bin/catalina.sh"
    put("/root/%s" %tomcat_name,remote_dir)
    with cd(remote_dir):
        run("tar -zxvf %s "%tomcat_name)
        run("set -m;%s start" %start_dir)
def stop_tomcat():
    run("ps -ef |grep java  |grep -v grep |awk '{print $2}' |xargs kill -9 ")
def backup_tomcat():
    remote_dir = "/data/tomcat/"
    tomcat_name = "apache-tomcat-8.0.45.tar.gz"
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_dir = "/data/backup-tomcat/"
    dir = backup_dir + date
    run("mkdir -pv %s" %dir)
    run("mv %s%s %s"%(remote_dir,tomcat_name,dir))
    run("rm -rf /data/tomcat/apache-tomcat-8.0.45")

def publish():
    getHostName()
    stop_tomcat()
    backup_tomcat()
    deploy()

