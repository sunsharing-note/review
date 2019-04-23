##### 安装alertmanager

* wget https://github.com/prometheus/alertmanager/releases/download/v0.16.2/alertmanager-0.16.2.linux-amd64.tar.gz
* tar -zxvf alertmanager-0.16.2.linux-amd64.tar.gz
* vim alertmanager.yml  ## 见alertmanager1.yml
* nohup  ./alertmanager --config.file=./alertmanager.yml &