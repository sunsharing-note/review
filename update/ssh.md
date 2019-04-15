```
yum install -y gcc zlib-devel openssl-devel
yum  -y install xinetd && yum -y install telnet-server


iptables -I INPUT -p tcp --dport 23 -j ACCEPT
sed -i 's/yes/no/g' /etc/xinetd.d/telnet
cat /etc/xinetd.d/telnet
systemctl restart telnet.socket && systemctl restart xinetd
service xinetd restart
ss -tnl
sed -i '$ a\pts\/1' /etc/securetty
sed -i '$ a\pts\/2' /etc/securetty
sed -i '$ a\pts\/3' /etc/securetty

cd /home/iotapp 
mv openssh_bak openssh_bak-0410
mv openssh openssh0410
mkdir openssh
tar -zxvf openssh-7.4p1.tar.gz
cd /home/iotapp/openssh-7.4p1 && ./configure  --prefix=/usr/local/openssh && make && make install
mkdir /home/iotapp/openssh_bak

echo "先备份"
mv /usr/sbin/sshd /home/iotapp/openssh_bak/
mv /usr/bin/ssh* /home/iotapp/openssh_bak/
mv /etc/init.d/sshd /home/iotapp/openssh_bak/sshd_start
mv /etc/ssh/ssh_host_ecdsa_key.pub /home/iotapp/openssh_bak/
cp /home/iotapp/openssh/etc/ssh_host_ecdsa_key.pub /etc/ssh/

echo "更新"
cp /usr/local/openssh/sbin/sshd /usr/sbin/
cp /usr/local/openssh/bin/ssh* /usr/bin/
cp /home/iotapp/openssh-7.4p1/opensshd.init /etc/init.d/sshd
cp /usr/local/openssh/etc/ssh_host_ecdsa_key.pub /etc/ssh/
chmod +x /etc/init.d/sshd
service sshd restart
ssh -V
ss -tnl
ssh -V

```