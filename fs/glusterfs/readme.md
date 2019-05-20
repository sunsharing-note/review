```
参考:https://baijiahao.baidu.com/s?id=1612194635156434300&wfr=spider&for=pc
文档中缺少 glusterfs volume start volume_name
1 GlusterFS搭建步骤
1.1涉及服务器
172.19.2.119-123
# 先安装 gluster 源
$ yum install centos-release-gluster -y

# 安装 glusterfs 组件
$ yum install -y glusterfs glusterfs-server glusterfs-fuse glusterfs-rdma glusterfs-geo-replication glusterfs-devel

## 创建 glusterfs 目录
$ mkdir /opt/glusterd

## 修改 glusterd 目录
$ sed -i 's/var\/lib/opt/g' /etc/glusterfs/glusterd.vol

# 启动 glusterfs
$ systemctl start glusterd.service

# 设置开机启动
$ systemctl enable glusterd.service

# 查看状态
$ systemctl status glusterd.service

# 创建存储目录
$ mkdir /opt/gfs_data

1.2 修改hosts
vim /etc/hosts
172.19.2.119 k8s-node1
172.19.2.120 k8s-node2
172.19.2.121 k8s-node3
172.19.2.122 k8s-node4
172.19.2.123 k8s-node5

1.3 加入集群节点，node1无需加入
gluster peer probe k8s-node2
gluster peer probe k8s-node3
gluster peer probe k8s-node4
gluster peer probe k8s-node5

[root@k8s-node1 ~]# gluster peer status
Number of Peers: 4

Hostname: k8s-node5
Uuid: 66168b48-19af-478c-b5ca-236ab58cdaf0
State: Peer in Cluster (Connected)

Hostname: k8s-node4
Uuid: c7fd5a5c-8cca-46c2-b9be-e59e7caf461f
State: Peer in Cluster (Connected)

Hostname: k8s-node3
Uuid: 3da3cc4b-962a-423a-8e1a-88d6028bf19c
State: Peer in Cluster (Connected)

Hostname: k8s-node2
Uuid: 581b198c-3e2e-45c1-8cc7-99edb48b062e
State: Peer in Cluster (Connected)


1.4 创建gluster卷，采用DHT模式，生产环境慎用
gluster volume create k8s-volume transport tcp k8s-node5:/opt/gfs_data k8s-node4:/opt/gfs_data k8s-node1:/opt/gfs_data force

[root@k8s-node1 ~]# gluster volume info
 
Volume Name: k8s-volume
Type: Distribute
Volume ID: 6618ff81-a7ae-4272-b8c3-4364f9195883
Status: Created
Snapshot Count: 0
Number of Bricks: 3
Transport-type: tcp
Bricks:
Brick1: k8s-node5:/opt/gfs_data
Brick2: k8s-node4:/opt/gfs_data
Brick3: k8s-node1:/opt/gfs_data
Options Reconfigured:
transport.address-family: inet
nfs.disable: on

1.5 扩容gluster卷
## 加 force 参数是因为报根目录路径无法添加的错误
gluster volume add-brick k8s-volume k8s-node3:/opt/gfs_data force
gluster volume add-brick k8s-volume k8s-node2:/opt/gfs_data force

2 Gluster部署到Kubernetes
2.1 创建Gluster Endpoint
glusterfs-endpoints.json
{
  "kind": "Endpoints",
  "apiVersion": "v1",
  "metadata": {
    "name": "glusterfs-cluster",
    "namespace": "default" 
  },
  "subsets": [
    {
      "addresses": [
        {
          "ip": "172.19.2.119"
        }
      ],
      "ports": [
        {
          "port": 1990    
        }
      ]
    }
  ]
}

2.2 创建Gluster服务
glusterfs-service.json
{
  "kind": "Service",
  "apiVersion": "v1",
  "metadata": {
    "name": "glusterfs-cluster"
  },
  "spec": {
    "ports": [
      {"port": 1900}
    ]
  }
}

2.3 创建PV
glusterfs-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: gluster-dev-volume
spec:
  capacity:
    storage: 8Gi
  accessModes:
    - ReadWriteMany
  glusterfs:
    endpoints: "glusterfs-cluster"
    path: "k8s-volume"
    readOnly: false

2.4 创建PVC
glusterfs-pvc.yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: glusterfs-nginx
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 8Gi

2.5 创建nginx示例deployment
nginx-dep.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-dm
spec:
  replicas: 2
  template:
    metadata:
      labels:
        name: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:alpine
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 80
          volumeMounts:
            - name: gluster-dev-volume
              mountPath: "/usr/share/nginx/html"
      volumes:
      - name: gluster-dev-volume
        persistentVolumeClaim:
          claimName: glusterfs-nginx

2.6 验证文件持久化存储
在nginx实例中创建 index.html
kubectl exec -it nginx-dm-7668bb95d4-62xmt -- touch /usr/share/nginx/html/index.html

查看具体存储到哪个节点
[root@k8s-node1 ~]# ansible kube-node -a "ls /opt/gfs_data"
172.19.2.121 | SUCCESS | rc=0 >>


172.19.2.123 | SUCCESS | rc=0 >>


172.19.2.119 | SUCCESS | rc=0 >>


172.19.2.122 | SUCCESS | rc=0 >>
index.html

172.19.2.120 | SUCCESS | rc=0 >>


3 GlusterFS相关知识补充
3.1 GlusterFS 几种 volume 模式说明
1. 默认模式，既 DHT, 也叫 分布卷: 将文件已 hash 算法随机分布到 一台服务器节点中存储。
gluster volume create test-volume server1:/exp1 server2:/exp2

2. 复制模式，既 AFR, 创建 volume 时带 replica x 数量: 将文件复制到 replica x 个节点中。
gluster volume create test-volume replica 2 transport tcp server1:/exp1 server2:/exp2

3. 条带模式，既 Striped, 创建 volume 时带 stripe x 数量： 将文件切割成数据块，分别存储到 stripe x 个节点中 (类似 raid 0)。
gluster volume create test-volume stripe 2 transport tcp server1:/exp1 server2:/exp2

4. 分布式条带模式（组合型），最少需要 4 台服务器才能创建。 创建 volume 时 stripe 2 server = 4 个节点： 是 DHT 与 Striped 的组合型。
gluster volume create test-volume stripe 2 transport tcp server1:/exp1 server2:/exp2 server3:/exp3 server4:/exp4

5. 分布式复制模式（组合型）, 最少需要 4 台服务器才能创建。 创建 volume 时 replica 2 server = 4 个节点：是 DHT 与 AFR 的组合型。
gluster volume create test-volume replica 2 transport tcp server1:/exp1 server2:/exp2　server3:/exp3 server4:/exp4

6. 条带复制卷模式（组合型）, 最少需要 4 台服务器才能创建。 创建 volume 时 stripe 2 replica 2 server = 4 个节点： 是 Striped 与 AFR 的组合型。
gluster volume create test-volume stripe 2 replica 2 transport tcp server1:/exp1 server2:/exp2 server3:/exp3 server4:/exp4

7. 三种模式混合, 至少需要 8 台 服务器才能创建。 stripe 2 replica 2 , 每 4 个节点 组成一个 组。
gluster volume create test-volume stripe 2 replica 2 transport tcp server1:/exp1 server2:/exp2 server3:/exp3 server4:/exp4 server5:/exp5 server6:/exp6 server7:/exp7 server8:/exp8

3.2 GlusterFS优化
# 开启 指定 volume 的配额
$ gluster volume quota k8s-volume enable

# 限制 指定 volume 的配额
$ gluster volume quota k8s-volume limit-usage / 1TB

# 设置 cache 大小, 默认32MB
$ gluster volume set k8s-volume performance.cache-size 4GB

# 设置 io 线程, 太大会导致进程崩溃
$ gluster volume set k8s-volume performance.io-thread-count 16

# 设置 网络检测时间, 默认42s
$ gluster volume set k8s-volume network.ping-timeout 10

# 设置 写缓冲区的大小, 默认1M
$ gluster volume set k8s-volume performance.write-behind-window-size 1024MB
```