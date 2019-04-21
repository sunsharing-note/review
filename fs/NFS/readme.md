```
因为 NFS 支持的功能相当的多，而不同的功能都会使用不同的程序来启动， 每启动一个功能就会启用一些端口来传输数据，因此， NFS 的功能所对应的端口才没有固定住， 而是随机取用一些未被使用的小于 1024 的埠口来作为传输之用。但如此一来又造成客户端想要连上服务器时的困扰， 因为客户端得要知道服务器端的相关埠口才能够联机吧！

此时我们就得需要远程过程调用 (RPC) 的服务啦！RPC 最主要的功能就是在指定每个 NFS 功能所对应的 port number ，并且回报给客户端，让客户端可以连结到正确的埠口上去。 那 RPC 又是如何知道每个 NFS 的埠口呢？这是因为当服务器在启动 NFS 时会随机取用数个埠口，并主动的向 RPC 注册，因此 RPC 可以知道每个埠口对应的 NFS 功能，然后 RPC 又是固定使用 port 111 来监听客户端的需求并回报客户端正确的埠口， 所以当然可以让 NFS 的启动更为轻松愉快了！

所以你要注意，要启动 NFS 之前，RPC 就要先启动了，否则 NFS 会无法向 RPC 注册。 另外，RPC 若重新启动时，原本注册的数据会不见，因此 RPC 重新启动后，它管理的所有服务都需要重新启动来重新向 RPC 注册。

当客户端有 NFS 档案存取需求时，他会如何向服务器端要求数据呢？

客户端会向服务器端的 RPC (port 111) 发出 NFS 档案存取功能的询问要求；
服务器端找到对应的已注册的 NFS daemon 埠口后，会回报给客户端；
客户端了解正确的埠口后，就可以直接与 NFS daemon 来联机。

由于 NFS 的各项功能都必须要向 RPC 来注册，如此一来 RPC 才能了解 NFS 这个服务的各项功能之 port number, PID, NFS 在服务器所监听的 IP 等等，而客户端才能够透过 RPC 的询问找到正确对应的埠口。 也就是说，NFS 必须要有 RPC 存在时才能成功的提供服务，因此我们称 NFS 为 RPC server 的一种。事实上，有很多这样的服务器都是向 RPC 注册的，举例来说，NIS (Network Information Service) 也是 RPC server 的一种呢

安装与配置:

1.检查是否之前有安装
rpm -qa | grep nfs
rpm -qa | grep rpcbind

2.安装
yum -y install nfs-utils rpcbind

3.配置
[root@bogon ~]# vim /etc/exports 
/data/lys 192.168.2.0/24(rw,no_root_squash,no_all_squash,sync)

常见的参数则有：

参数值    内容说明
rw　　ro    该目录分享的权限是可擦写 (read-write) 或只读 (read-only)，但最终能不能读写，还是与文件系统的 rwx 及身份有关。

sync　　async    sync 代表数据会同步写入到内存与硬盘中，async 则代表数据会先暂存于内存当中，而非直接写入硬盘！

no_root_squash　　root_squash    客户端使用 NFS 文件系统的账号若为 root 时，系统该如何判断这个账号的身份？预设的情况下，客户端 root 的身份会由 root_squash 的设定压缩成 nfsnobody， 如此对服务器的系统会较有保障。但如果你想要开放客户端使用 root 身份来操作服务器的文件系统，那么这里就得要开 no_root_squash 才行！

all_squash    不论登入 NFS 的使用者身份为何， 他的身份都会被压缩成为匿名用户，通常也就是 nobody(nfsnobody) 啦！

anonuid　　anongid    anon 意指 anonymous (匿名者) 前面关于 *_squash 提到的匿名用户的 UID 设定值，通常为 nobody(nfsnobody)，但是你可以自行设定这个 UID 的值！当然，这个 UID 必需要存在于你的 /etc/passwd 当中！ anonuid 指的是 UID 而 anongid 则是群组的 GID 啰。

4.配置生效
[root@bogon lys]# exportfs -r

5.启动服务

service rpcbind start
service nfs start

查看rpc服务注册情况
rpcinfo -p localhost

6.安装客户端
yum -y install nfs-utils

挂在
mount -t nfs 192.168.2.203:/data/lys /lys -o proto=tcp -o nolock


7.固定nfs端口

vim /etc/sysconfig/nfs

RQUOTAD_PORT=30001
LOCKD_TCPPORT=30002
LOCKD_UDPPORT=30002
MOUNTD_PORT=30003
STATD_PORT=30004
```