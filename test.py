#! /usr/bin/env python
# -*- coding: utf-8 -*-


li = [{'hostid': '11139', 'name': 'zkho', 'interfaces': [{'ip': '163.53.93.114'}]}]

dic1 = {}

dic1["name"] = li[0]["name"]
dic1["ip"] = li[0]["interfaces"][0]["ip"]

print(dic1)