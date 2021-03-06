* https://www.jdon.com/51223
* 1.Docker与虚拟机有何不同？
* docker设计小巧，部署迁移快速，运行高效，应用之间相互独立，管理人员可以看到所有容器的内容，虚拟化技术比较臃肿，不论什么应用都需要先创建新的系统，并且并非按照应用隔离，而是按照系统隔离，管理员无法看到系统内部信息。
* 与虚拟机不同，容器不需要引导操作系统内核，因此可以在不到一秒的时间内创建容器。此功能使基于容器的虚拟化比其他虚拟化方法更加独特和可取;由于基于容器的虚拟化为主机增加了很少或没有开销，因此基于容器的虚拟化具有接近本机的性能;对于基于容器的虚拟化，与其他虚拟化不同，不需要其他软件;主机上的所有容器共享主机的调度程序，从而节省了额外资源的需求;与虚拟机映像相比，容器状态（Docker或LXC映像）的大小很小，因此容器映像很容易分发;容器中的资源管理是通过cgroup实现的。Cgroups不允许容器消耗比分配给它们更多的资源。虽然主机的所有资源都在虚拟机中可见，但无法使用。这可以通过在容器和主机上同时运行top或htop来实现。所有环境的输出看起来都很相似。
* 2.Docker的工作原理
* 每个容器都在自己的命名空间中运行，但使用与所有其他容器完全相同的内核。发生隔离是因为内核知道分配给进程的命名空间，并且在API调用期间确保进程只能访问其自己的命名空间中的资源。
* 3.什么是Docker？
* Docker是一个容器化平台，它以容器的形式将您的应用程序及其所有依赖项打包在一起，以确保您的应用程序在开发，测试或生产的任何环境中无缝运行；Docker容器，将一个软件包装在一个完整的文件系统中，该文件系统包含运行所需的一切：代码，运行时，系统工具，系统库等可以安装在服务器上的任何东西；
* 4.如何使用Docker构建与环境无关的系统？
* Volumes  环境变量注入  只读文件系统
* 5.什么是Docker镜像？
* Docker镜像是Docker容器的源代码。换句话说，Docker镜像用于创建容器。使用build命令创建映像，并且在使用run启动时它们将生成容器。镜像存储在Docker注册表registry.hub.docker.com中，因为它们可能变得非常大，镜像被设计为由其他镜像层组成，允许在通过网络传输镜像时发送最少量的数据。
* 6.什么是Docker容器？
* Docker容器包括应用程序及其所有依赖项，但与其他容器共享内核，作为主机操作系统上用户空间中的独立进程运行。Docker容器不依赖于任何特定的基础架构：它们可以在任何计算机，任何基础架构和任何云中运行。
* 7.什么是Docker Hub？
* Docker hub是一个基于云的注册表服务，允许您链接到代码存储库，构建镜像并测试它们，存储手动推送的镜像以及指向Docker云的链接，以便您可以将镜像部署到主机。它为整个开发流程中的容器镜像发现，分发和变更管理，用户和团队协作以及工作流自动化提供了集中资源。
* 8.Docker容器有几种状态？
* 运行 已暂停 重新启动 已退出
* 9.什么类型的应用程序 - 无状态或有状态更适合Docker容器？
* 最好为Docker Container创建无状态应用程序。我们可以从应用程序中创建一个容器，并从应用程序中取出可配置的状态参数。现在我们可以在生产和具有不同参数的QA环境中运行相同的容器。这有助于在不同场景中重用相同的图像。使用Docker Containers比使用有状态应用程序更容易扩展无状态应用程序。
* 10.解释基本的Docker使用流程
* 一切都从Dockerfile开始。Dockerfile是镜像的源代码
* 创建Dockerfile后，您可以构建它以创建容器的镜像。镜像只是“源代码”的“编译版本”，即Dockerfile
* 获得容器的镜像后，应使用注册表重新分发容器。注册表就像一个git存储库 - 你可以推送和拉取镜像
* 接下来，您可以使用该镜像来运行容器。在许多方面，正在运行的容器与虚拟机（但没有管理程序）非常相似
* 11.Dockerfile中最常见的指令是什么？​​​​​​​
* FROM RUN LABEL CMD
* 12.Dockerfile中的命令COPY和ADD命令有什么区别？
* 一般而言，虽然ADD并且COPY在功能上类似，但是COPY是优选的。那是因为它比ADD更透明。COPY仅支持将本地文件基本复制到容器中，而ADD具有一些功能（如仅限本地的tar提取和远程URL支持），这些功能并不是很明显。因此，ADD的最佳用途是将本地tar文件自动提取到镜像中，如ADD rootfs.tar.xz /中所示。
* 13.Docker镜像和层有什么区别？
* 镜像：Docker镜像是由一系列只读层构建的
* 层：每个层代表镜像Dockerfile中的一条指令
* 14.解释一下dockerfile的ONBUILD指令？
* 当镜像用作另一个镜像构建的基础时，ONBUILD指令向镜像添加将在稍后执行的触发指令。
* 15.构建Docker镜像应该遵循哪些原则？
* 尽量选取满足需求但较小的基础系统镜像
* 清理编译生成文件、安装包的缓存等临时文件
* 安装各个软件时候要指定准确的版本号，并避免引入不需要的依赖
* 从安全的角度考虑，应用尽量使用系统的库和依赖
* 使用Dockerfile创建镜像时候要添加.dockerignore文件或使用干净的工作目录
* 16.如何临时退出一个正在交互的容器的终端，而不终止它？
* 按Ctrl+p，后按Ctrl+q，如果按Ctrl+c会使容器内的应用进程终止，进而会使容器终止。
* 17.Docker的macvlan overlan
* 当容器需要直连入物理网络时，可以使用Macvlan。有两种桥接模式:Bridge模式：不创建子接口的情况下直接去桥接物理接口。直接桥接到与宿主级的同网段。VLAN Bridge模式：创建子接口去桥接物理接口。可划分多个VLAN。
* 创建：docker network create -d macvlan --subnet 192.168.29.0/24 --gateway 192.168.29.2 -o parent=ens33 -o macvlan_mode=bridge macnet 使用：docker run -id --net macnet --ip 192.168.29.7 --name tomcat1 tomcat sh
* 特点：1.两个容器间互通 2.主机1与主机2的容器通 主机2与主机1的容器通 3.主机与其上的容器不通
* overlay 网络驱动程序在多个 Docker 守护进程主机之间创建一个分布式网络。这个网络在允许容器连接并进行安全通信的主机专用网络之上（overlay 覆盖在上面）。Docker 透明地处理每个 Docker 守护进程与目标容器之间的数据包的路由。
* 
* 18.docker的隔离方式
* Mount Namespace 提供磁盘挂载点和文件系统的隔离能力 IPC Namespace 提供进程间通信的隔离能力 Network Namespace 提供网络隔离能力 UTS Namespace 提供主机名隔离能力 PID Namespace 提供进程隔离能力 User Namespace 提供用户隔离能力
* 19.Docker中的防火墙zone
* 完全开放：--privileged=true 部分开放：--cap-add NET_ADMIN --cap-add NET_RAW
* 20.docker volume
* 如果要在容器之间共享数据，最好是使用 data container。Flocker：容器的分布式存储平台
* 21.docker创建镜像方式
* docker commit(已经运行的容器) docker build