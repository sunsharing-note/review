##### cni插件作用

* 保证每个Pod拥有一个集群内唯一的IP地址
* 保证不同节点的IP地址划分不会重复
* 保证垮节点的Pod可以互相通信
* 保证不同节点的Pod可以与垮节点的主机互相通信

```
docker可配置的网络:

none：将容器添加到一个容器专门的网络堆栈中，没有对外连接。

host：将容器添加到主机的网络堆栈中，没有隔离。

default bridge：默认网络模式。每个容器可以通过IP地址相互连接。

自定义网桥：用户定义的网桥，具有更多的灵活性、隔离性和其他便利功能

网络术语：

第2层网络： OSI（Open Systems Interconnections，开放系统互连）网络模型的“数据链路”层。第2层网络会处理网络上两个相邻节点之间的帧传递。第2层网络的一个值得注意的示例是以太网，其中MAC表示为子层。

第3层网络： OSI网络模型的“网络”层。第3层网络的主要关注点，是在第2层连接之上的主机之间路由数据包。IPv4、IPv6和ICMP是第3层网络协议的示例。

VXLAN：代表“虚拟可扩展LAN”。首先，VXLAN用于通过在UDP数据报中封装第2层以太网帧来帮助实现大型云部署。VXLAN虚拟化与VLAN类似，但提供更大的灵活性和功能（VLAN仅限于4096个网络ID）。VXLAN是一种封装和覆盖协议，可在现有网络上运行。

Overlay网络：Overlay网络是建立在现有网络之上的虚拟逻辑网络。Overlay网络通常用于在现有网络之上提供有用的抽象，并分离和保护不同的逻辑网络。

封装：封装是指在附加层中封装网络数据包以提供其他上下文和信息的过程。在overlay网络中，封装被用于从虚拟网络转换到底层地址空间，从而能路由到不同的位置（数据包可以被解封装，并继续到其目的地）。

网状网络：网状网络（Mesh network）是指每个节点连接到许多其他节点以协作路由、并实现更大连接的网络。网状网络允许通过多个路径进行路由，从而提供更可靠的网络。网状网格的缺点是每个附加节点都会增加大量开销。

BGP：代表“边界网关协议”，用于管理边缘路由器之间数据包的路由方式。BGP通过考虑可用路径，路由规则和特定网络策略，帮助弄清楚如何将数据包从一个网络发送到另一个网络。BGP有时被用作CNI插件中的路由机制，而不是封装的覆盖网络。



flannel:

特点：
Flannel相对容易安装和配置

Flannel配置第3层IPv4 overlay网络。它会创建一个大型内部网络，跨越集群中每个节点。在此overlay网络中，每个节点都有一个子网，用于在内部分配IP地址。在配置pod时，每个节点上的Docker桥接口都会为每个新容器分配一个地址。同一主机中的Pod可以使用Docker桥接进行通信，而不同主机上的pod会使用flanneld将其流量封装在UDP数据包中，以便路由到适当的目标

默认vxlan，因为VXLAN性能更良好并且需要的手动干预更少



calico:

calico包括如下重要组件：Felix，etcd，BGP Client，BGP Route Reflector。下面分别说明一下这些组件。

Felix：主要负责路由配置以及ACLS规则的配置以及下发，它存在在每个node节点上。

etcd：分布式键值存储，主要负责网络元数据一致性，确保Calico网络状态的准确性，可以与kubernetes共用；

BGPClient(BIRD), 主要负责把 Felix写入 kernel的路由信息分发到当前 Calico网络，确保 workload间的通信的有效性；

BGPRoute Reflector(BIRD), 大规模部署时使用，摒弃所有节点互联的mesh模式，通过一个或者多个 BGPRoute Reflector 来完成集中式的路由分发；

特点：
Calico不使用overlay网络，Calico配置第3层网络，该网络使用BGP路由协议在主机之间路由数据包。这意味着在主机之间移动时，不需要将数据包包装在额外的封装层中。BGP路由机制可以本地引导数据包，而无需额外在流量层中打包流量。

标准调试工具可以访问与简单环境中相同的信息，从而使更多开发人员和管理员更容易理解行为。

Calico还可以与服务网格Istio集成，以便在服务网格层和网络基础架构层中解释和实施集群内工作负载的策略。这意味着用户可以配置强大的规则，描述pod应如何发送和接受流量，提高安全性并控制网络环境
```