```
mkdir /opt/prometheus
cd /opt/prometheus
wget https://github.com/prometheus/prometheus/releases/download/v1.7.1/prometheus-1.7.1.linux-amd64.tar.gz
tar -zxvf prometheus-1.7.1.linux-amd64.tar.gz
vim prometheus-1.7.1.linux-amd64/prometheus.yml
nohup  /opt/prometheus/prometheus-1.7.1.linux-amd64/prometheus  -config.file=/opt/prometheus/prometheus-1.7.1.linux-amd64/prometheus.yml &

node-expoter:
cd /opt/
mkdir prometheus_exporters
cd prometheus_exporters
wget https://github.com/prometheus/node_exporter/releases/download/v0.14.0/node_exporter-0.14.0.linux-amd64.tar.gz
tar -zxvf node_exporter-0.14.0.linux-amd64.tar.gz
nohup  /opt/prometheus_exporters/node_exporter-0.14.0.linux-amd64/node_exporter &

mysql-expoter:
mkdir -p /opt/prometheus_expoters
cd /opt/prometheus_expoters
wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.10.0/mysqld_exporter-0.10.0.linux-amd64.tar.gz
tar -zxvf mysqld_exporter-0.10.0.linux-amd64.tar.gz
cd mysqld_exporter-0.10.0.linux-amd64/
vim .my.cnf
nohup  /opt/prometheus_expoters/mysqld_exporter-0.10.0.linux-amd64/mysqld_exporter -config.mf-cnf=.my.cnf &
```