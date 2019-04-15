mkdir  /home/iotapp/openssh_20190410
mv /etc/ssh/ssh_host_ecdsa_key.pub  /home/iotapp/openssh_20190410/ 
mv /usr/sbin/sshd /home/iotapp/openssh_20190410/
mv /usr/bin/ssh* /home/iotapp/openssh_20190410/
mv /etc/init.d/sshd /home/iotapp/openssh_20190410/sshd-start

cp /home/iotapp/openssh_bak/sshd /usr/sbin/
cp /home/iotapp/openssh_bak/ssh* /usr/bin/
cp /home/iotapp/openssh_bak/sshd_start  /etc/init.d/sshd
cp /home/iotapp/openssh_bak/ssh_host_ecdsa_key.pub /etc/ssh/