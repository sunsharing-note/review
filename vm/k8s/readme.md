#### Kubernetes主要由以下几个核心组件组成 https://www.kubernetes.org.cn/daemonset

* etcd保存了整个集群的状态
* apiserver提供了资源操作的唯一入口，并提供认证、授权、访问控制、API注册和发现等机制
* controller manager负责维护集群的状态，比如故障检测、自动扩展、滚动更新等
* scheduler负责资源的调度，按照预定的调度策略将Pod调度到相应的机器上
* kubelet负责维护容器的生命周期，同时也负责Volume（CVI）和网络（CNI）的管理
* Container runtime负责镜像管理以及Pod和容器的真正运行（CRI）
* kube-proxy负责为Service提供cluster内部的服务发现和负载均衡

#### Add-ons

* kube-dns负责为整个集群提供DNS服务
* Ingress Controller为服务提供外网入口
* Heapster(新版本已经使用metric-server)提供资源监控
* Dashboard提供GUI
* Federation提供跨可用区的集群
* Fluentd-elasticsearch提供集群日志采集、存储与查询

#### 分层架构
* 核心层：Kubernetes最核心的功能，对外提供API构建高层的应用，对内提供插件式应用执行环境
* 应用层：部署（无状态应用、有状态应用、批处理任务、集群应用等）和路由（服务发现、DNS解析等）
* 管理层：系统度量（如基础设施、容器和网络的度量），自动化（如自动扩展、动态Provision等）以及策略管理（RBAC、Quota、PSP、NetworkPolicy等）
* 接口层：kubectl命令行工具、客户端SDK以及集群联邦
* Kubernetes外部：日志、监控、配置管理、CI、CD、Workflow、FaaS、OTS应用、ChatOps等
* Kubernetes内部：CRI、CNI、CVI、镜像仓库、Cloud Provider、集群自身的配置和管理等

#### 名词解释

1. pod 在Kubernetes中，最小的管理元素不是一个个独立的容器，而是Pod,Pod是最小的，管理，创建，计划的最小单元.一个Pod相当于一个共享context的配置组，在同一个context下，应用可能还会有独立的cgroup隔离机制，一个Pod是一个容器环境下的“逻辑主机”，它可能包含一个或者多个紧密相连的应用。支持三种RestartPolicy：Always：只要退出就重启 OnFailure：失败退出（exit code不等于0）时重启 Never：只要退出就不再重启 注意，这里的重启是指在Pod所在Node上面本地重启，并不会调度到其他Node上去。支持三种ImagePullPolicy：Always：不管镜像是否存在都会进行一次拉取。Never：不管镜像是否存在都不会进行拉取。IfNotPresent：只有镜像不存在时，才会进行镜像拉取。默认为IfNotPresent，但:latest标签的镜像默认为Always。Kubernetes提供了两种探针：LivenessProbe：探测应用是否处于健康状态，如果不健康则删除重建改容器；ReadinessProbe：探测应用是否启动完成并且处于正常服务状态，如果不正常则更新容器的状态。支持Probe，支持exec、tcp和httpGet方式。容器生命周期钩子（Container Lifecycle Hooks）监听容器生命周期的特定事件，并在事件发生时执行已注册的回调函数。支持两种钩子：postStart： 容器启动后执行，注意由于是异步执行，它无法保证一定在ENTRYPOINT之后运行。如果失败，容器会被杀死，并根据RestartPolicy决定是否重启;preStop：容器停止前执行，常用于资源清理。如果失败，容器同样也会被杀死。通过nodeSelector，一个Pod可以指定它所想要运行的Node节点。可以通过给Pod增加kubernetes.io/ingress-bandwidth和kubernetes.io/egress-bandwidth这两个annotation来限制Pod的网络带宽。可以通过nodeSelector、nodeAffinity、podAffinity以及Taints和tolerations等来将Pod调度到需要的Node上。
2. service service能够让前台持续的追踪到这些后台。Service 是一个定义了一组Pod的策略的抽象。这些被服务标记的Pod都是（一般）通过label Selector决定的。Kubernetes 支持两种方式的来发现服务 ，环境变量和 DNS。
3. volume 一个Kubernetes volume，拥有明确的生命周期，与所在的Pod的生命周期相同。因此，Kubernetes volume独立与任何容器，与Pod相关，所以数据在重启的过程中还会保留，当然，如果这个Pod被删除了，那么这些数据也会被删除。更重要的是，Kubernetes volume 支持多种类型，任何容器都可以使用多个Kubernetes volume。它的核心，一个 volume 就是一个目录，可能包含一些数据，这些数据对pod中的所有容器都是可用的，这个目录怎么使用，什么类型，由什么组成都是由特殊的volume 类型决定的。一个容器崩溃了不会导致数据的丢失，因为容器的崩溃并不移除pod. 
4. deployment Deployment为Pod和ReplicaSet提供了一个声明式定义(declarative)方法.Deployment在生命周期中有多种状态。在创建一个新的ReplicaSet的时候它可以是 progressing 状态， complete 状态，或者fail to progress状态。
5. namespace Namespace是对一组资源和对象的抽象集合，比如可以用来将系统内部的对象划分为不同的项目组或用户组。常见的pods, services, replication controllers和deployments等都是属于某一个namespace的（默认是default），而node, persistentVolumes等则不属于任何namespace。
6. labels 标签其实就一对 key/value ，被关联到对象上，标签的使用我们倾向于能够标示对象的特殊特点，并且对用户而言是有意义的，标签可以用来划分特定组的对象。API目前支持两种选择器：基于相等的和基于集合的。基于相等性或者不相等性的条件允许用label的键或者值进行过滤，有三种运算符是允许的，“=”，“==”和“!=”。前两种代表相等性（他们是同义运算符），后一种代表非相等性。基于集合的label条件允许用一组值来过滤键。支持三种操作符: in ， notin ,和 exists(仅针对于key符号) 。
7. Replication Controller Replication Controller 保证了在所有时间内，都有特定数量的Pod副本正在运行。就像一个进程管理器，监管着不同node上的多个pod,而不是单单监控一个node上的pod,Replication Controller 会委派本地容器来启动一些节点上服务（Kubelet ,Docker）。只会对那些RestartPolicy = Always的Pod的生效
8. node Node是Pod真正运行的主机，可以物理机，也可以是虚拟机。为了管理Pod，每个Node节点上至少要运行container runtime（比如docker或者rkt）、kubelet和kube-proxy服务。Kubernetes只是管理Node上的资源.Node Controller负责维护Node状态 与Cloud Provider同步Node 给Node分配容器CIDR 删除带有NoExecute taint的Node上的Pods,默认情况下，kubelet在启动时会向master注册自己，并创建Node资源。每个Node都包括以下状态信息:地址：包括hostname、外网IP和内网IP 条件（Condition）：包括OutOfDisk、Ready、MemoryPressure和DiskPressure 容量（Capacity）：Node上的可用资源，包括CPU、内存和Pod总数 基本信息（Info）：包括内核版本、容器引擎版本、OS类型等
9. pv pvc sc PersistentVolume（PV）是集群中已由管理员配置的一段网络存储。PersistentVolumeClaim（PVC）是用户存储的请求。StorageClass为管理员提供了一种描述他们提供的存储的“类”的方法。PV和PVC之间的相互作用遵循这个生命周期:Provisioning ——-> Binding ——–>Using——>Releasing——>Recycling。卷将处于以下阶段之一：Faild Released Available Bound
10. secret Secret解决了密码、token、密钥等敏感数据的配置问题，而不需要把这些敏感数据暴露到镜像或者Pod Spec中。Secret可以以Volume或者环境变量的方式使用。Secret有三种类型：Service Account Opaque kubernetes.io/dockerconfigjson
11. statefulset StatefulSet是为了解决有状态服务的问题,其应用场景包括稳定的持久化存储，即Pod重新调度后还是能访问到相同的持久化数据，基于PVC来实现  稳定的网络标志，即Pod重新调度后其PodName和HostName不变，基于Headless Service（即没有Cluster IP的Service）来实现  有序部署，有序扩展，即Pod是有顺序的，在部署或者扩展的时候要依据定义的顺序依次依次进行（即从0到N-1，在下一个Pod运行之前所有之前的Pod必须都是Running和Ready状态），基于init containers来实现  有序收缩，有序删除（即从N-1到0）.从上面的应用场景可以发现，StatefulSet由以下几个部分组成：用于定义网络标志（DNS domain）的Headless Service  用于创建PersistentVolumes的volumeClaimTemplates  定义具体应用的StatefulSet 注意：StatefulSet需要一个Headless Service来定义DNS domain，需要在StatefulSet之前创建好
12. daemonset DaemonSet保证在每个Node上都运行一个容器副本，常用来部署一些集群的日志、监控或者其他系统管理应用。典型的应用包括：日志收集，比如fluentd，logstash等 系统监控，比如Prometheus Node Exporter，collectd，New Relic agent，Ganglia gmond等 系统程序，比如kube-proxy, kube-dns, glusterd, ceph等
13. serviceaccount Service account是为了方便Pod里面的进程调用Kubernetes API或其他外部服务而设计的。
14. Security Context的目的是限制不可信容器的行为，保护系统和其他容器不受其影响。Kubernetes提供了三种配置Security Context的方法：Container-level Security Context：仅应用到指定的容器  Pod-level Security Context：应用到Pod内所有容器以及Volume  Pod Security Policies（PSP）：应用到集群内部所有Pod以及Volume
15. 资源配额（Resource Quotas）是用来限制用户资源用量的一种机制。它的工作原理为资源配额应用在Namespace上，并且每个Namespace最多只能有一个ResourceQuota对象  开启计算资源配额后，创建容器时必须配置计算资源请求或限制（也可以用LimitRange设置默认值） 用户超额后禁止创建新的资源
16. Network Policy提供了基于策略的网络控制，用于隔离应用并减少攻击面。
17. Ingress就是为进入集群的请求提供路由规则的集合.Ingress可以给service提供集群外部访问的URL、负载均衡、SSL终止、HTTP路由等。
18. ConfigMap用于保存配置数据的键值对，可以用来保存单个属性，也可以用来保存配置文件。
19. HPA 可以根据CPU使用率或应用自定义metrics自动扩展Pod数量.支持三种metrics类型：预定义metrics（比如Pod的CPU）以利用率的方式计算  自定义的Pod metrics，以原始值（raw value）的方式计算  自定义的object metrics