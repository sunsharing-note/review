#!/usr/bin/env python
#--coding:utf-8--





menu = {
    "sc":{
        "cmccsq-v2-device": {
            "201801": {"count": 1},
            "201802": {"count": 2},
        },
        "cmccsq-v2-web": {
            "201801": {"count": 1},
            "201802": {"count": 2},
        },
        "cmccsq_v2_app_http": {
            "201801": {"count": 1},
            "201802": {"count": 2},
        },
    },
    "router":{
        "router-center-api": {
            "201801": {"count": 1},
            "201802": {"count": 2},
        },
        "route-job":{
            "201801": {"count": 1},
            "201802": {"count": 2},
        },
    },
}

current_layer = menu
parent_layers = []
while True:
    for key in current_layer:
        print(key)
    choice = input(">>>>>:")
    
    if len(choice) == 0:
        continue
    if choice in current_layer:
        #parent_layer = current_layer
        parent_layers.append(current_layer)
        current_layer = current_layer[choice]
    elif choice == "b":
#        current_layer = parent_layer
        if parent_layers:
            current_layer = parent_layers.pop()
    elif choice == "q":
        exit("退出")
    
    else:
        print("没有这个")