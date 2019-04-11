* nginx的负载均衡依赖于ngx_http_upstream_module
* 支持的代理方式:proxy_pass fastcgi_pass(和动态程序交互) memcached_pass(缓存)
* 放在http{}标签内
* 默认算法是wrr(权重轮询)
* 可选参数 1 server ip:port 2 weight 3 max_fails=xx 4 backup 5 failtimeout=20s 6 down 7 max_conn
*  