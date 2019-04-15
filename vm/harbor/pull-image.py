#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __Time__    : 2019/3/7 21:53
# __Author__  : Allen_Jol
# __Software__: PyCharm

import os

S_registry = 'registry.cn-hangzhou.aliyuncs.com/allen_k8s/'
D_registry = 'k8s.gcr.io/'
Login_Registry = 'docker login --username=lifu@1551256880623472 --password=jianglifu1101..! registry.cn-hangzhou.aliyuncs.com'
os.system(Login_Registry)

master_images = ['kube-apiserver:v1.13.4','kube-controller-manager:v1.13.4',
                 'kube-scheduler:v1.13.4','kube-proxy:v1.13.4','pause:3.1',
                 'etcd:3.2.24','coredns:1.2.6','flannel:v0.10.0-amd64'
                ]

# 下载镜像
def Pull_Images(registry,images):
    print("一共 %s 个镜像" %(len(master_images),))
    os.system('sleep 2')
    index = 1
    for image in images:
        print("开始下载第 %d 个镜像 ---> %s" % (index,image))
        pull_cmd = "docker pull " + registry + image
        os.popen(pull_cmd)
        print("pull 第 %s 个 image done!" % (index))
        index +=1

def Tag_Images(sregistry,dregistry,images):
    print("一共 %s 个镜像" % (len(images)),)
    index = 1
    for image in images:
        print("开始tag第 %d 个镜像 ---> 源镜像名字: %s,目标镜像名字: %s" %(index,sregistry+image,dregistry+image))
        tag_cmd = "docker tag " + sregistry + image + dregistry + image + " " + dregistry + image
        os.popen(tag_cmd)
        print("tag 第 %s 个镜像 done!" % (index))
        index += 1

# Run Pull_Images.py
if __name__ == '__main__':
    Pull_Images(S_registry,master_images)
    Tag_Images(S_registry,D_registry,master_images)