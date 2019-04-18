```
cd /opt/
mkdir grafana
wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana-4.3.2-1.x86_64.rpm
rpm -ivh grafana-4.3.2-1.x86_64.rpm
vim /etc/grafana/grafana.ini
systemctl daemon-reload
systemctl enable grafana-server.service
systemctl start grafana-server.service
```