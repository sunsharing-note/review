```
VIP地址ping不通,需要注释vrrp_strict参数配置即可!

1.VRRP全称Virtual Router Redundancy Protocol，即虚拟路由冗余协议。对于VRRP，需要清楚知道的是：
1）VRRP是用来实现路由器冗余的协议。
2）VRRP协议是为了消除在静态缺省路由环境下路由器单点故障引起的网络失效而设计的主备模式的协议，使得发生故障而进行设计设备功能切换时可以不影响内外数据通信，不需要再修改内部网络的网络参数。
3）VRRP协议需要具有IP备份，优先路由选择，减少不必要的路由器通信等功能。
4）VRRP协议将两台或多台路由器设备虚拟成一个设备，对外提供虚拟路由器IP（一个或多个）。然而，在路由器组内部，如果实际拥有这个对外IP的路由器如果工作正常的话，就是master，或者是通过算法选举产生的，MASTER实现针对虚拟路由器IP的各种网络功能，如ARP请求，ICMP，以及数据的转发等，其他设备不具有该IP，状态是BACKUP。除了接收MASTER的VRRP状态通告信息外，不执行对外的网络功能，当主级失效时，BACKUP将接管原先MASTER的网络功能。
5）VRRP协议配置时，需要配置每个路由器的虚拟路由ID(VRID)和优先权值，使用VRID将路由器进行分组，具有相同VRID值的路由器为同一个组，VRID是一个0-255的整整数，；同一个组中的路由器通过使用优先权值来选举MASTER。，优先权大者为MASTER，优先权也是一个0-255的正整数

2.keepalived工作原理
keepalived可提供vrrp以及health-check功能，可以只用它提供双机浮动的vip（vrrp虚拟路由功能），这样可以简单实现一个双机热备高可用功能；keepalived是以VRRP虚拟路由冗余协议为基础实现高可用的，可以认为是实现路由器高可用的协议，即将N台提供相同功能的路由器组成一个路由器组，这个组里面有一个master和多个backup，master上面有一个对外提供服务的vip（该路由器所在局域网内其他机器的默认路由为该vip），master会发组播，当backup收不到VRRP包时就认为master宕掉了，这时就需要根据VRRP的优先级来选举一个backup当master。这样的话就可以保证路由器的高可用了。
keepalived也是模块化设计，不同模块复杂不同的功能，它主要有三个模块，分别是core、check和VRRP，其中：
core模块：为keepalived的核心组件，负责主进程的启动、维护以及全局配置文件的加载和解析；
check：负责健康检查，包括常见的各种检查方式；
VRRP模块：是来实现VRRP协议的。

3.Keepalived作用
Keepalived主要用作RealServer的健康状态检查以及LoadBalance主机和BackUP主机之间failover的实现。Keepalived的作用是检测web服务器的状态，如果有一台web服务器死机，或工作出现故障，Keepalived将检测到，并将有故障的web服务器从系统中剔除，当web服务器工作正常后Keepalived自动将web服务器加入到服务器群中，这些工作全部自动完成，不需要人工干涉，需要人工做的只是修复故障的web服务器。

4.Keepalived和Heartbeat之间的对比
1）Keepalived使用更简单：从安装、配置、使用、维护等角度上对比，Keepalived都比Heartbeat要简单得多，尤其是Heartbeat2.1.4后拆分成3个子项目，安装、配置、使用都比较复杂，尤其是出问题的时候，都不知道具体是哪个子系统出问题了；而Keepalived只有1个安装文件、1个配置文件，配置文件也简单很多；
2）Heartbeat功能更强大：Heartbeat虽然复杂，但功能更强大，配套工具更全，适合做大型集群管理，而Keepalived主要用于集群倒换，基本没有管理功能；
3）协议不同：Keepalived使用VRRP协议进行通信和选举，Heartbeat使用心跳进行通信和选举；Heartbeat除了走网络外，还可以通过串口通信，貌似更可靠；
Keepalived使用的vrrp协议方式，虚拟路由冗余协议 ；Heartbeat是基于主机或网络的服务的高可用方式；
Keepalived的目的是模拟路由器的双机；Heartbeat的目的是用户service的双机
4）使用方式基本类似：如果要基于两者设计高可用方案，最终都要根据业务需要写自定义的脚本，Keepalived的脚本没有任何约束，随便怎么写都可以；Heartbeat的脚本有约束，即要支持service start/stop/restart这种方式，而且Heartbeart提供了很多默认脚本，简单的绑定ip，启动apache等操作都已经有了；

使用建议：
优先使用Keepalived，当Keepalived不够用的时候才选择Heartbeat
lvs的高可用建议用Keepavlived
业务的高可用用Heartbeat


state：state指定instance(Initial)的初始状态，就是说在配置好后，这台服务器的初始状态就是这里指定的，但这里指定的不算，还是得要通过竞选通过优先级来确定，里如果这里设置为master，但如若他的优先级不及另外一台，那么这台在发送通告时，会发送自己的优先级，另外一台发现优先级不如自己的高，那么他会就回抢占为master
interface：实例绑定的网卡，因为在配置虚拟IP的时候必须是在已有的网卡上添加的
dont track primary：忽略VRRP的interface错误
track interface：跟踪接口，设置额外的监控，里面任意一块网卡出现问题，都会进入故障(FAULT)状态，例如，用nginx做均衡器的时候，内网必须正常工作，如果内网出问题了，这个均衡器也就无法运作了，所以必须对内外网同时做健康检查
mcast src ip：发送多播数据包时的源IP地址，这里注意了，这里实际上就是在那个地址上发送VRRP通告，这个非常重要，一定要选择稳定的网卡端口来发送，这里相当于heartbeat的心跳端口，如果没有设置那么就用默认的绑定的网卡的IP，也就是interface指定的IP地址
garp master delay：在切换到master状态后，延迟进行免费的ARP(gratuitous ARP)请求
virtual router id：这里设置VRID，这里非常重要，相同的VRID为一个组，他将决定多播的MAC地址
priority 100：设置本节点的优先级，优先级高的为master
advert int：检查间隔，默认为1秒
virtual ipaddress：这里设置的就是VIP，也就是虚拟IP地址，他随着state的变化而增加删除，当state为master的时候就添加，当state为backup的时候删除，这里主要是有优先级来决定的，和state设置的值没有多大关系，这里可以设置多个IP地址
virtual routes：原理和virtual ipaddress一样，只不过这里是增加和删除路由
lvs sync daemon interface：lvs syncd绑定的网卡
authentication：这里设置认证
auth type：认证方式，可以是PASS或AH两种认证方式
auth pass：认证密码
nopreempt：设置不抢占，这里只能设置在state为backup的节点上，而且这个节点的优先级必须别另外的高
preempt delay：抢占延迟
debug：debug级别
notify master：和sync group这里设置的含义一样，可以单独设置，例如不同的实例通知不同的管理人员，http实例发给网站管理员，mysql的就发邮件给DBA



```