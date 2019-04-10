#! /usr/bin/env python

import re


tags = ['latest', '20180612.16.20', '20180510.18.16',
 '20180608.14.34', '20180510.18.26',
 '20180510.21.56', '20180531.08.54', '201805101623',
 '20180608.14.31', '20180510.17.32', '20180608.16.55',
  '201805101627', '20180510.17.18']


seri = "201806"
tag = []
for i in tags:
    ret = re.findall("%s.*" % seri,i)
    print(type(ret))
    if not ret:
        continue
    else:
        tag.append(ret)
print(tag)


























# li = [{'id': 1, 'name': 'library'}, 
# {'id': 2, 'name': 'sc'}, 
# {'id': 3, 'name': 'smart_pallet'}, 
# {'id': 5, 'name': 'router'}, 
# {'id': 7, 'name': 'ops'}, 
# {'id': 8, 'name': 'test'}, 
# {'id': 9, 'name': 'gcr.io'}, 
# {'id': 10, 'name': 'wuyigc'}, 
# {'id': 11, 'name': 'business'}
# ]

# for i in li:
#     if i["id"] == 11:
#         print(i["name"])

# li = [10, 12, 2, 9, 7, 5]
# flag = 2 in li
# print(flag)

# tags1 = ['201810', '201903', '201812', '201810', '201810',
#  '201810', '201811', '201810', 'latest', '201811', '201810',
#   '201812', '201812', '201810', '201810', '201810', '201812', 
#   '201810', '201812', '201811', '201810', '201810', '201812', 
#   '201811', '201811', '201903',
#  '201901', '201811', '201812', '201901', '201812']
# tags2 = []
# [tags2.append(i) for i in tags1 if not i  in tags2]
# # print(tags2)
# tags3 = {}
# for i in tags2:
#     print("count for %s is %s:" %(i,tags1.count(i)))
#     tags3["name"] = i
#     tags3["count"] = tags1.count(i)
#     print(tags3)