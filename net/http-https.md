##### 参考:https://www.cnblogs.com/chenliyang/p/6558756.html

* HTTP是Hyper Text Transfer Protocol（超文本传输协议）的缩写
* HTTP协议是一个无状态的协议，同一个客户端的这次请求和上次请求是没有对应关系
* 一次HTTP操作称为一个事务，其工作过程可分为四步：
* 1.首先客户机与服务器需要建立连接。只要单击某个超级链接，HTTP的工作开始
* 2.建立连接后，客户机发送一个请求给服务器，请求方式的格式为：统一资源标识符（URL）、协议版本号，后边是MIME信息包括请求修饰符、客户机信息和可能的内容
* 3.服务器接到请求后，给予相应的响应信息，其格式为一个状态行，包括信息的协议版本号、一个成功或错误的代码，后边是MIME信息包括服务器信息、实体信息和可能的内容
* 4.客户端接收服务器所返回的信息通过浏览器显示在用户的显示屏上，然后客户机与服务器断开连接
* 补充：如果在以上过程中的某一步出现错误，那么产生错误的信息将返回到客户端，有显示屏输出。对于用户来说，这些过程是由HTTP自己完成的，用户只要用鼠标点击，等待信息显示就可以了
* 

