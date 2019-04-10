```
# centos7.x master与backup安装配置大同小异
yum repolist
yum -y install keepalived
mkdir /etc/keepalived
cd /etc/keepalived/
mv keepalived.conf keepalived.conf.bak
vim keepalived.conf
vim ck_ng.sh
chmod +x ck_ng.sh
systemctl enable keepalived.service
rpm -ivh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
yum -y install nginx
systemctl enable nginx.service
service nginx start
vim /usr/share/nginx/html/index.html
curl localhost
service keepalived start
curl 192.168.29.100
service keepalived stop
curl 192.168.29.100
service keepalived start
service keepalived status
```