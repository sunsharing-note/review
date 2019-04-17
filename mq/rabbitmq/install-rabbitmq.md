### basic-installed

* 安装erlang: yum -y install erlang
* import keys:rpm --import https://www.rabbitmq.com/rabbitmq-release-signing-key.asc
* 安装rabbitmq: yum install rabbitmq-server-3.7.9-1.el7.noarch.rpm
* 下载rabbitmq:wget https://dl.bintray.com/rabbitmq/all/rabbitmq-server/3.7.4/rabbitmq-server-3.7.4-1.el7.noarch.rpm
* 查看状态：service rabbitmq-server status
* 启动：service rabbitmq-server start
* 停止：service rabbitmq-server stop
* 查看状态：rabbitmqctl status
* 启用插件：rabbitmq-plugins enable rabbitmq_management
* 重启：service rabbitmq-server restart
* 添加用户和密码：rabbitmqctl add_user name passwd
* 添加管理员角色：rabbitmqctl set_user_tags admin administrator
* 赋予权限：rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"

### cluster
```
1、安装rabbit:假设已经按照上述方式安装了三台rabbit
2、集群：
node1:
vim /etc/rabbitmq/rabbit-env.conf
cat /etc/rabbitmq/rabbit-env.conf
HOME=/var/lib/rabbitmq
service rabbitmq-server restart(都重启一下)
把rabbit-env.conf复制到另外的节点
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl start_app
node2:
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl join_cluster --disc rabbit@ansible-node1
rabbitmqctl start_app
node3:
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl join_cluster --disc rabbit@ansible-node1
rabbitmqctl start_app
添加用户：
rabbitmqctl add_user admin 123456
rabbitmqctl set_user_tags admin administrator
rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
rabbitmqctl list_users
更换节点类型：
rabbitmqctl stop_app
rabbitmqctl change_cluster_node_type ram
rabbitmqctl change_cluster_node_type disc
rabbitmqctl start_app
移除节点：
rabbitmqctl stop_app
rabbitmqctl restart
rabbitmqctl start_app
集群重启顺序：
启动顺序：磁盘节点 => 内存节点
关闭顺序：内存节点 => 磁盘节点
```