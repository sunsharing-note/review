* Perl双引号和单引号的区别: 双引号可以正常解析一些转义字符与变量，而单引号无法解析会原样输出

* perl数据类型： 标量: $myfirst=123;  数组: @arr=(1,2,3); 哈希: %h=("a"=>1,"b"=>2);
* perl转义字符: \\  \' \" \a \b \f \n \r \t  \v \0nn \cnn \cX \u \l \U \L \Q \E
* .用来连接字符串
*  __FILE__, __LINE__, 和 __PACKAGE__ 分别表示当前执行脚本的文件名，行号，包名 __ 是两条下划线，__FILE__ 前后各两条下划线
*  一个以 v 开头,后面跟着一个或多个用句点分隔的整数,会被当作一个字串文本
*  sec min hour mday mon year wday yday isdst
*  my(局部) local(临时) state(静态)
*  引用就是指针，Perl 引用是一个标量类型可以指向变量、数组、哈希表（也叫关联数组）甚至子程序，可以应用在程序的任何地方
*  format stdout =      .
*  unlink rename tell