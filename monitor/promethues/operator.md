* operator作用:通过Kubernetes原生提供的应用管理概念实现自动化
* Operator就是针对管理特定应用程序的，帮助用户创建，配置和管理复杂的有状态应用程序。从而实现特定应用程序的常见操作以及运维自动化。
* operator提供了四类资源:
* 1.Prometheus：声明式创建和管理Prometheus Server实例
* 2.ServiceMonitor：负责声明式的管理监控配置
* 3.PrometheusRule：负责声明式的管理告警配置
* 4.Alertmanager：声明式的创建和管理Alertmanager实例
* 