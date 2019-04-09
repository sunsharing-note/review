* 环境 redhat7.6 默认使用的是firewalld 而不是iptables 以下是使用iptbales
* 安装iptables: yum install iptables-services 禁用firewalld:systemctl mask firewalld 启用iptables:systemctl enable iptables
* systemctl相当于之前service和chkconfig的融合体
* 启动iptables:systemctl start iptables
* systemctl systemd-cgls

```
启动服务：systemctl start iptables 
关闭服务：systemctl stop iptables 
重启服务：systemctl restart iptables 
显示服务状态：systemctl status iptables 
在开机时启用服务：systemctl enable iptables 
在开机时禁用服务：systemctl disable iptables 
查看服务是否开机启动：systemctl is-enabled iptables 
查看已启动的服务列表：systemctl list-unit-files|grep enabled 
查看启动失败的服务列表：systemctl –failed
systemctl mask firewalld  #屏蔽服务
systemctl unmask firewalld #显示服务

raw：高级功能，如：网址过滤。
mangle：数据包修改（QOS），用于实现服务质量。
net：地址转换，用于网关路由器。
filter：包过滤，用于防火墙规则。

INPUT链：处理输入数据包。
OUTPUT链：处理输出数据包。
PORWARD链：处理转发数据包。
PREROUTING链：用于目标地址转换（DNAT）。
POSTOUTING链：用于源地址转换（SNAT）

accept：接收数据包。
DROP：丢弃数据包。
REDIRECT：重定向、映射、透明代理。
SNAT：源地址转换。
DNAT：目标地址转换。
MASQUERADE：IP伪装（NAT），用于ADSL。
LOG：日志记录

iptables -F    #清除所选链中的所有规则
iptables -Z    #指定链的计数器，清零
iptables -X    #删除用户自定义的规则链
举个例子：iptables -t nat -F  #清空nat表规制

-p：指定匹配的数据包协议类型
=== tcp 、 udp 、 icmp 装载协议 
=== sport ：source 源端口 
=== dport ：dst 目标端口
-A 追加
-I 在现有规则上面添加
-D 删除

```
* 放开端口: iptables -A  INPUT -p tcp --dport 22 -j ACCEPT
* 禁止ping: iptables -A INPUT -p icmp -j DROP
* 允许ping: iptables -A INPUT -p icmp -j ACCEPT
* 删除某条规则: iptables -D INPUT -p icmp -j ACCEPT
* 禁止往外ping: iptables -A OUTPUT -p icmp -j DROP
* 禁止某个ip或着某类 telnet: iptables -I INPUT -s 192.168.31.100 -p tcp --dport 22 -j DROP
* 禁止所有: iptables -A INPUT -p tcp -j DROP
* 允许所有: iptables -I INPUT -p tcp -j ACCEPT 或者删除禁止所有的规则 iptables -D INPUT -p tcp -j DROP
* FORWARD链的默认规则是DROP
* OUTPUT链默认规则是ACCEPT
* INPUT链的默认规则是DROP
* 
