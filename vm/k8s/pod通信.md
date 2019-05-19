* pod内容器访问: 通过localhost 共享了网络命名空间
* pod之间的访问: 1.在同一主机: 因为关联到了同一个docker0网桥，所以可以访问;2.在不同主机：利用cni插件，
node1的docker0-->flannel0--->node2的flannel0--->docker0