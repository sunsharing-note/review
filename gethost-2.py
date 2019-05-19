#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import re
import time
import datetime
import os,sys



# 获取登录token
def getToken(url, header, username, password):
    data = {"jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": username,
                "password": password
            },
            "id": 1,
            "auth": None
            }
    request = requests.post(url=url, headers=header, data=json.dumps(data))
    return json.loads(request.content)["result"]



# 获取sla
def getSla(url, header, token,timeStamp2,timeStamp1):
    data = {
        "jsonrpc": "2.0",
        "method": "service.getsla",
        "params": {
            "serviceids": "41",
            "intervals": [
                {
                    "from": timeStamp2,
                    "to": timeStamp1
                }
            ]
        },
        "auth": token,
        "id": 1
    }

    sla = requests.post(url=url, headers=header, data=json.dumps(data))
    #print(type(json.loads(sla.content)["result"]))
    return json.loads(sla.content)["result"]

# 获取所有主机
def getHost(url, header, token):
    data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": [
                "hostid",
                "host"
            ],
            "selectInterfaces": [
                "interfaceid",
                "ip"
            ]
        },
        "id": 2,
        "auth": token
    }
    # print(token)
    # hosss = requests.post(url=url,headers=header,data=json.dumps(data))
    # return json.loads(hosss.content)["result"]
    hosts = requests.post(url=url, headers=header, data=json.dumps(data))
    return json.loads(hosts.content)["result"]


# 获取所有ip
def getIp(hosts):
    ret = re.findall("(\d{1,3}\.\d+\.\d+\.\d+)", hosts)
    return ret


# 写到hosts.txt文件中
def writeHost(host):
    with open("hosts.txt", "a", encoding="utf8") as  ho:
        host = list(set(host))
        host.sort()
        for i in host:
            ho.write("%s\n" % i)



url = "http://1xxxx/api_jsonrpc.php"
#url = "https://xxxxxxxxxxxxxxx/zabbix/api_jsonrpc.php"
header = {"Content-Type": "application/json-rpc"}
username = "zhouhua"
password = "abcd1234"
token = getToken(url, header, username, password)
print(token)
hosts = str(getHost(url, header, token))
host = getIp(hosts)
print(host)
# 写进文本中
writeHost(host)
#now_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
#now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#print(now_time)
# 1天前时间
#to_time = datetime.datetime.now()+ datetime.timedelta(days=-1)

#to_time2 = to_time.strftime("%Y-%m-%d %H:%M:%S")
#print(to_time2)
# 当前时间的时间戳
#timeArray1 = time.strptime(now_time,"%Y-%m-%d %H:%M:%S")
#timeStamp1 = time.mktime(timeArray1)
# 7天前时间的时间戳
#timeArray2 = time.strptime(to_time2,"%Y-%m-%d %H:%M:%S")
#timeStamp2 = time.mktime(timeArray2)
#sla = round(getSla(url,header,token,timeStamp2,timeStamp1)["41"]["sla"][0]["sla"],2)
#print(type(sla))
#print(round(sla,2))

#print(os.path.abspath(__file__))
#print(os.path.dirname(os.path.abspath(__file__)))
#print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# path = os.path.dirname(os.path.abspath(__file__))
# sla_txt = path.join("/sanfei-sla.txt")
# 2019-02-27 项目：三费 sla:xxx
