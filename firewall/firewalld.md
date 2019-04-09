#####  install

```
yum -y install firewalld firewall-config
systemctl status firewalld 
systemctl start firewalld
systemctl enable firewalld

yum -y install firewalld firewall-config #安装firewalld
systemctl enable|disable firewalld #开机启动
systemctl start|stop|restart firewalld #启动、停止、重启firewalld

--permanent 永久生效 需要 --reload

firewall-cmd --version 查看firewalld版本
firewall-cmd --help 查看firewall-cmd用法
man firewall-cmd

firewall-cmd --state #查看firewalld的状态
systemctl status firewalld #查看firewalld的状态,详细

firewall-cmd --reload 重新载入防火墙配置，当前连接不中断
firewall-cmd --complete-reload 重新载入防火墙配置，当前连接中断

firewall-cmd --get-services 列出所有预设服务
firewall-cmd --list-services 列出当前服务
firewall-cmd --permanent --zone=public --add-service=smtp 启用服务
firewall-cmd --permanent --zone=public --remove-service=smtp 禁用服务

firewall-cmd --zone=public --list-ports 
firewall-cmd --permanent --zone=public --add-port=8080/tcp 启用端口
firewall-cmd --permanent --zone=public --remove-port=8080/tcp 禁用端口
firewall-cmd --zone="public" --add-forward-port=port=80:proto=tcp:toport=12345 同服务器端口转发 80端口转发到12345端口
firewall-cmd --zone=public --add-masquerade 不同服务器端口转发，要先开启 masquerade
firewall-cmd --zone="public" --add-forward-port=port=80:proto=tcp:toport=8080:toaddr=192.168.1.1 不同服务器端口转发，转发到192.168.1.1的8080端口

firewall-cmd --get-zones 查看所有可用区域
firewall-cmd --get-active-zones 查看当前活动的区域,并附带一个目前分配给它们的接口列表
firewall-cmd --list-all-zones 列出所有区域的所有配置
firewall-cmd --zone=work --list-all 列出指定域的所有配置
firewall-cmd --get-default-zone 查看默认区域
firewall-cmd --set-default-zone=public 设定默认区域

firewall-cmd --get-zone-of-interface=eno222
firewall-cmd [--zone=<zone>] --add-interface=<interface> 添加网络接口
firewall-cmd [--zone=<zone>] --change-interface=<interface> 修改网络接口
firewall-cmd [--zone=<zone>] --remove-interface=<interface> 删除网络接口
firewall-cmd [--zone=<zone>] --query-interface=<interface> 查询网络接口

firewall-cmd --permanent --zone=internal --add-source=192.168.122.0/24 设置网络地址到指定的区域
firewall-cmd --permanent --zone=internal --remove-source=192.168.122.0/24 删除指定区域中的网路地址

firewall-cmd --get-icmptypes

firewall-cmd –list-rich-rules 列出所有规则
firewall-cmd [–zone=zone] –query-rich-rule=’rule’ 检查一项规则是否存在
firewall-cmd [–zone=zone] –remove-rich-rule=’rule’ 移除一项规则
firewall-cmd [–zone=zone] –add -rich-rule=’rule’ 新增一

firewall-cmd --zone=public --add-rich-rule 'rule family="ipv4" source address=192.168.0.14 accept' 允许来自主机 192.168.0.14 的所有 IPv4 流量
firewall-cmd --zone=public --add-rich-rule 'rule family="ipv4" source address="192.168.1.10" port port=22 protocol=tcp reject' 拒绝来自主机 192.168.1.10 到 22 端口的 IPv4 的 TCP 流量
firewall-cmd --zone=public --add-rich-rule 'rule family=ipv4 source address=10.1.0.3 forward-port port=80 protocol=tcp to-port=6532' 许来自主机 10.1.0.3 到 80 端口的 IPv4 的 TCP 流量，并将流量转发到 6532 端口上
firewall-cmd --zone=public --add-rich-rule 'rule family=ipv4 forward-port port=80 protocol=tcp to-port=8080 to-addr=172.31.4.2' 将主机 172.31.4.2 上 80 端口的 IPv4 流量转发到 8080 端口（需要在区域上激活 masquerade）
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.122.0" accept' 允许192.168.122.0/24主机所有连接
firewall-cmd --add-rich-rule='rule service name=ftp limit value=2/m accept' 每分钟允许2个新连接访问ftp服务
firewall-cmd --add-rich-rule='rule service name=ftp log limit value="1/m" audit accept' 同意新的IPv4和IPv6连接FTP ,并使用审核每分钟登录一次
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.122.0/24" service name=ssh log prefix="ssh" level="notice" limit value="3/m" accept' 允许来自1192.168.122.0/24地址的新IPv4连接连接TFTP服务,并且每分钟记录一次
firewall-cmd --permanent --add-rich-rule='rule protocol value=icmp drop' 丢弃所有icmp包
firewall-cmd --add-rich-rule='rule family=ipv4 source address=192.168.122.0/24 reject' --timeout=10 当使用source和destination指定地址时,必须有family参数指定ipv4或ipv6。如果指定超时,规则将在指定的秒数内被激活,并在之后被自动移除
firewall-cmd --add-rich-rule='rule family=ipv6 source address="2001:db8::/64" service name="dns" audit limit value="1/h" reject' --timeout=300 拒绝所有来自2001:db8::/64子网的主机访问dns服务,并且每小时只审核记录1次日志
firewall-cmd --permanent --add-rich-rule='rule family=ipv4 source address=192.168.122.0/24 service name=ftp accept' 允许192.168.122.0/24网段中的主机访问ftp服务
firewall-cmd --add-rich-rule='rule family="ipv6" source address="1:2:3:4:6::" forward-portto-addr="1::2:3:4:7" to-port="4012" protocol="tcp" port="4011"' 转发来自ipv6地址1:2:3:4:6::TCP端口4011,到1:2:3:4:7的TCP端口4012
firewall-cmd –direct –add-rule ipv4 filter IN_public_allow 0 -p tcp –dport 80 -j ACCEPT 添加规则
firewall-cmd –direct –remove-rule ipv4 filter IN_public_allow 10 -p tcp –dport 80 -j ACCEPT 删除规则
firewall-cmd –direct –get-all-rules 列出规则
```<!-- slide -->

