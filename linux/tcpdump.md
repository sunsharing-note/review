* tcpdump  -n -i ens33 host 192.168.29.133
* tcpdump  -n -i ens33 src host 192.168.29.133
* tcpdump -i eth1 dst host 192.168.29.162
* tcpdump -n -i eth0 port 8080
* tcpdump -i eth1 -s 0 -l -w - dst port 3306 | strings
* tcpdump -n -nn -tttt -i eth0 -s 65535 'port 3306' -w 20160505mysql.cap
* tcpdump -i eth1 'tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack != 0'
* tcpdump -i eth1 'tcp[(tcp[12]>>2):4] = 0x47455420'
* tcpdump -i eth1 'tcp[(tcp[12]>>2):4] = 0x5353482D'
* tcpdump -i eth0 '((port 8080) and (tcp[(tcp[12]>>2):4]=0x47455420))' -nnAl -w /tmp/GET.log
* time tcpdump -nn -i eth0 'tcp[tcpflags] = tcp-syn' -c 10
