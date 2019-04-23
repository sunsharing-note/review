##### 关联alert与prome


* 在prometheus.yml中加入以下内容:(详见prometheus.yml)
  
```
alerting:
  alertmanagers:
    - static_configs:
      - targets: ['192.168.29.132:9093']
```