#!/bin/bash
d=`date --date today +%Y%m%d_%H:%M:%S`
n=`ps -C nginx --no-heading|wc -l`
if [ $n -eq "0" ]; then
        systemctl start nginx
        n2=`ps -C nginx --no-heading|wc -l`
        if [ $n2 -eq "0"  ]; then
                echo "$d nginx down,keepalived will stop" >> /var/log/check_ng.log
                systemctl stop keepalived
        fi
fi