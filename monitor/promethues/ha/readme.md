* 本地存储劣势: 数据持久化 不适合保存大量历史数据 无法进行弹性扩展
* 为了解决本地存储的问题:Prometheus提供了remote_write和remote_read的特性，支持将数据存储到远端和从远端读取数据。通过将监控与数据分离，Prometheus能够更好地进行弹性扩展
* 联邦集群的特性可以让Prometheus将样本采集任务划分到不同的Prometheus实例中，并且通过一个统一的中心节点进行聚合，从而可以使Prometheuse可以根据规模进行扩展
* prometheus:将两小时内产生的数据存储在一个块(Block)中，每一个块中包含该时间窗口内的所有样本数据(chunks)，元数据文件(meta.json)以及索引文件(index)。
* 如果Prometheus发生崩溃或者重启时能够恢复数据，Prometheus启动时会从写入日志(WAL)进行重播，从而恢复数据
* Remote Storage
* Adaptor
* 实现自定义Remote Storage需要用户分别创建用于支持remote_read和remote_write的HTTP服务
* 下面以influxdb作remote_storage
* 1.这里使用docker-compose，详见docker-compose.yml
* 2.启动和查看:docker-compose up -d && docker ps -a
* 3.获取remote_storage_adopter:go get github.com/prometheus/prometheus/documentation/examples/remote_storage/remote_storage_adapter
* 启动适配器:INFLUXDB_PW=prom   /root/go/bin/remote_storage_adapter --influxdb-url=http://localhost:8086 --influxdb.username=prom   --influxdb.database=prometheus --influxdb.retention-policy=autogen &
* 4.修改prometheus.yml，添加配置:remote_write:
  
```
remote_write:
  - url: "http://localhost:9201/write"

remote_read:
  - url: "http://localhost:9201/read"
```

* 5.重启prometheus
* 6.查看数据:influx -username prom -password prom  -database prometheus  -execute 'show measurements'
* 7.测试：停止prometheus，删除data目录，重启验证
* Alertmanager引入了Gossip机制.Gossip机制为多个Alertmanager之间提供了信息传递的机制。确保及时在多个Alertmanager分别接收到相同告警信息的情况下，也只有一个告警通知被发送给Receiver。
* Gossip有两种实现方式分别为Push-based和Pull-based。
* 服务发现
* 服务注册软件:Consul.Consul是由HashiCorp开发的一个支持多数据中心的分布式服务发现和键值对存储服务的开源软件，被大量应用于基于微服务的软件架构当中。
* 基于文件的服务发现
* Relabel
* 在采集样本数据之前，对Target实例的标签进行重写的机制在Prometheus被称为Relabeling.instance与__address__就是标签的重写
* Prometheus允许用户在采集任务设置中通过relabel_configs来添加自定义的Relabeling过程
* 