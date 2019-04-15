
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
* 5.rc/rs 功能是怎么实现的？
* 6.deployment/rs 有什么区别。其使用方式、使用条件和原理是什么？
* 7.cgroup 中的 cpu 有哪几种限制方式。k8s 是如何使用实现 request 和 limit 的？