
* 原文地址：https://blog.csdn.net/qq_36357820/article/details/88954421
* 1.kubernetes 包含几个组件。各个组件的功能是什么。组件之间是如何交互的?
* etcd保存了整个集群的状态
* apiserver提供了资源操作的唯一入口，并提供认证、授权、访问控制、API注册和发现等机制
* controller manager负责维护集群的状态，比如故障检测、自动扩展、滚动更新等
* scheduler负责资源的调度，按照预定的调度策略将Pod调度到相应的机器上
* kubelet负责维护容器的生命周期，同时也负责Volume（CVI）和网络（CNI）的管理
* Container runtime负责镜像管理以及Pod和容器的真正运行（CRI）
* kube-proxy负责为Service提供cluster内部的服务发现和负载均衡
* 各组件之间相互合作来保证几群的正常运行
* 2.k8s 的 pause 容器有什么用？
* 每个Pod里运行着一个特殊的被称之为Pause的容器，其他容器则为业务容器，这些业务容器共享Pause容器的网络栈和Volume挂载卷，因此他们之间通信和数据交换更为高效，在设计时我们可以充分利用这一特性将一组密切相关的服务进程放入同一个Pod中。同一个Pod里的容器之间仅需通过localhost就能互相通信。PID命名空间：Pod中的不同应用程序可以看到其他应用程序的进程ID。网络命名空间：Pod中的多个容器能够访问同一个IP和端口范围。IPC命名空间：Pod中的多个容器能够使用SystemV IPC或POSIX消息队列进行通信。UTS命名空间：Pod中的多个容器共享一个主机名；Volumes（共享存储卷）：Pod中的各个容器可以访问在Pod级别定义的Volumes。
* 3.k8s 的 service 和 ep 是如何关联和相互影响的？
* k8s会根据service关联到pod的podIP信息组合成一个endpoint。若service定义中没有selector字段，service被创建时，endpoint controller不会自动创建endpoint。
* 4.详述 kube-proxy 原理，一个请求是如何经过层层转发落到某个 pod 上的整个过程。请求可能来自 pod 也可能来自外部？
* kube-proxy其实就是管理service的访问入口，包括集群内Pod到Service的访问和集群外访问service。 k8s提供了两种方式进行服务发现：环境变量和DNS。kube-proxy当前实现了两种proxyMode：userspace和iptables。iptables mode因为使用iptable NAT来完成转发，也存在不可忽视的性能损耗。userspace:service的请求会先从用户空间进入内核iptables，然后再回到用户空间，由kube-proxy完成后端Endpoints的选择和代理工作，这样流量从用户空间进出内核带来的性能损耗是不可接受的。
* 5.rc/rs 功能是怎么实现的？
* ReplicaSet和 Replication Controller之间的唯一区别是现在的选择器支持。Replication Controller只支持基于等式的selector（env=dev或environment!=qa），但ReplicaSet还支持新的，基于集合的selector（version in (v1.0, v2.0)或env notin (dev, qa)）。在试用时官方推荐ReplicaSet。
* 6.deployment/rs 有什么区别。其使用方式、使用条件和原理是什么？
* 如果您想要滚动更新功能，请考虑使用Deployments。此外， rolling-update命令是必须的，而Deployments是声明式的，因此我们建议通过rollout命令使用Deployments。Deployments拥有并管理ReplicaSets。
* 7.cgroup 中的 cpu 有哪几种限制方式。k8s 是如何使用实现 request 和 limit 的？
* 在cgroup里面，跟CPU相关的子系统有cpusets、cpuacct和cpu。cpu.cfs_period_us & cpu.cfs_quota_us cpu.shares cpu.stat.
* 目前CPU支持设置request和limit，memory只支持设置request， limit必须强制等于request。limits.cpu会被转换成docker的–cpu-quota参数，limits.memory会被转换成docker的–memory参数。
* 8.如何在 Kubernetes 中实现负载均衡？
* kube-proxy ingress
* 9.如何实现 Kubernetes 自动化?
* 日志 自我修复 弹性测试 常规审计 自动缩放 资源分配 容器资源限制
* 10.Pod 亲和性作用是什么？
* NodeSelector(定向调度)、NodeAffinity(Node亲和性)、PodAffinity(Pod亲和性)。
* 11.你能举例说明何时使用 Init Container 么？
* 当我们在运用一个服务之前，通常会做一些初始化的工作，而这些工作一般只需要运行一次，成功后就不再运行。特点：仅运行一次，成功后就会退出。 每个容器必须在成功执行完成后，系统才能继续执行下一个容器。 如果Init Container运行失败，kubernetes 将会重复重启Pod,直到Init Container 成功运行，但是如果 Pod的重启策略（restartPolicy）设置为Never,则Pod不会重启。 Init Container支持普通应用Container的所有参数，包括资源限制，挂载卷，安全设置等。但是Init Container 在资源的申请和限制上略有不同，同时，由于Init Container必须在Pod ready之前完成并退出，所以它不支持 readiness 探针。 Init Container 通常有如下应用方式：处于安全的考虑，可以将自定义的代码和工具使用Init Container运行，而不必添加到 应用 容器的镜像中；应用程序映像的构建和部署者角色可以彼此独立，无需共同构建单个应用程序映像；使用不同的Linux命名空间，可以使它们具有来自应用容器的不同文件系统权限。 因此，Init Container可以获得应用程序容器无法访问的Secrets；Init Container在任何应用程序容器启动之前运行完毕，而应用程序容器通常是并行运行的，因此初始容器提供了一种简单的方法来阻止或延迟应用程序容器的启动，直到满足一些前提条件。
* 12.什么是 Kubernetes Operator？
* Operator就是一系列应用程序特定的自定义控制器。允许用户编写的应用程序能够完整管理其他应用程序,Operator监控并且分析集群，同时基于一系列参数，触发一系列行为来达到所需状态。
* 13.服务和 ingress 的作用是什么？
* Service 是后端真实服务的抽象，一个 Service 可以代表多个相同的后端服务
* Ingress 是反向代理规则，用来规定 HTTP/S 请求应该被转发到哪个 Service 上，比如根据请求中不同的 Host 和 url 路径让请求落到不同的 Service 上
* Ingress Controller 就是一个反向代理程序，它负责解析 Ingress 的反向代理规则，如果 Ingress 有增删改的变动，所有的 Ingress Controller 都会及时更新自己相应的转发规则，当 Ingress Controller 收到请求后就会根据这些规则将请求转发到对应的 Service。
* 14.istio是一个专用的基础设施层，使得服务间的通信安全、高效和可靠