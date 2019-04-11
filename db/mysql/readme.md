## MVCC即多版本并发控制

```


https://blog.csdn.net/u013252072/article/details/52912385
1、MySQL的复制原理以及流程
基本原理流程，3个线程以及之间的关联；

2、MySQL中myisam与innodb的区别，至少5点
(1)、问5点不同；
(2)、innodb引擎的4大特性
(3)、2者selectcount(*)哪个更快，为什么

3、MySQL中varchar与char的区别以及varchar(50)中的50代表的涵义
(1)、varchar与char的区别
(2)、varchar(50)中50的涵义
(3)、int（20）中20的涵义
(4)、mysql为什么这么设计

4、问了innodb的事务与日志的实现方式
(1)、有多少种日志；
(2)、事物的4种隔离级别
(3)、事务是如何通过日志来实现的，说得越深入越好。

5、问了MySQL binlog的几种日志录入格式以及区别
(1)、binlog的日志格式的种类和分别
(2)、适用场景；
(3)、结合第一个问题，每一种日志格式在复制中的优劣。

6、问了下MySQL数据库cpu飙升到500%的话他怎么处理？
(1)、没有经验的，可以不问；
(2)、有经验的，问他们的处理思路。

7、sql优化
(1)、explain出来的各种item的意义；
(2)、profile的意义以及使用场景；

8、备份计划，mysqldump以及xtranbackup的实现原理
(1)、备份计划；
(2)、备份恢复时间；
(3)、xtrabackup实现原理

9、mysqldump中备份出来的sql，如果我想sql文件中，一行只有一个insert....value()的话，怎么办？如果备份需要带上master的复制点信息怎么办？

10、500台db，在最快时间之内重启
.
11、innodb的读写参数优化
(1)、读取参数
(2)、写入参数；
(3)、与IO相关的参数；
(4)、缓存参数以及缓存的适用场景。

12、你是如何监控你们的数据库的？你们的慢日志都是怎么查询的？
.
13、你是否做过主从一致性校验，如果有，怎么做的，如果没有，你打算怎么做？

14、你们数据库是否支持emoji表情，如果不支持，如何操作？
.
15、你是如何维护数据库的数据字典的?

16、你们是否有开发规范，如果有，如何执行的

17、表中有大字段X(例如：text类型)，且字段X不会经常更新，以读为为主，请问
(1)、您是选择拆成子表，还是继续放一起；
(2)、写出您这样选择的理由。

18、MySQL中InnoDB引擎的行锁是通过加在什么上完成(或称实现)的？为什么是这样子的？
.
19、如何从mysqldump产生的全库备份中只恢复某一个库、某一张表？

开放性问题：据说是腾讯的
一个6亿的表a，一个3亿的表b，通过外间tid关联，你如何最快的查询出满足条件的第50000到第50200中的这200条数据记录。


Part4:答案
1、MySQL的复制原理以及流程
基本原理流程，3个线程以及之间的关联；
1. 主：binlog线程——记录下所有改变了数据库数据的语句，放进master上的binlog中；
2. 从：io线程——在使用start slave 之后，负责从master上拉取 binlog 内容，放进 自己的relay log中；
3. 从：sql执行线程——执行relay log中的语句；

2、MySQL中myisam与innodb的区别，至少5点
(1)、问5点不同；
1>.InnoDB支持事物，而MyISAM不支持事物
2>.InnoDB支持行级锁，而MyISAM支持表级锁
3>.InnoDB支持MVCC, 而MyISAM不支持
4>.InnoDB支持外键，而MyISAM不支持
5>.InnoDB不支持全文索引，而MyISAM支持。

(2)、innodb引擎的4大特性
插入缓冲（insert buffer),二次写(double write),自适应哈希索引(ahi),预读(read ahead)
(3)、2者selectcount(*)哪个更快，为什么
myisam更快，因为myisam内部维护了一个计数器，可以直接调取。

3、MySQL中varchar与char的区别以及varchar(50)中的50代表的涵义
(1)、varchar与char的区别
char是一种固定长度的类型，varchar则是一种可变长度的类型
(2)、varchar(50)中50的涵义
最多存放50个字符，varchar(50)和(200)存储hello所占空间一样，但后者在排序时会消耗更多内存，因为order by col采用fixed_length计算col长度(memory引擎也一样)
(3)、int（20）中20的涵义
是指显示字符的长度
但要加参数的，最大为255，比如它是记录行数的id,插入10笔资料，它就显示00000000001 ~~~00000000010，当字符的位数超过11,它也只显示11位，如果你没有加那个让它未满11位就前面加0的参数，它不会在前面加0
20表示最大显示宽度为20，但仍占4字节存储，存储范围不变；
(4)、mysql为什么这么设计
对大多数应用没有意义，只是规定一些工具用来显示字符的个数；int(1)和int(20)存储和计算均一样；

4、问了innodb的事务与日志的实现方式
(1)、有多少种日志；
错误日志：记录出错信息，也记录一些警告信息或者正确的信息。
查询日志：记录所有对数据库请求的信息，不论这些请求是否得到了正确的执行。
慢查询日志：设置一个阈值，将运行时间超过该值的所有SQL语句都记录到慢查询的日志文件中。
二进制日志：记录对数据库执行更改的所有操作。
中继日志：
事务日志：

(2)、事物的4种隔离级别
隔离级别
读未提交(RU)
读已提交(RC)
可重复读(RR)
串行

(3)、事务是如何通过日志来实现的，说得越深入越好。
事务日志是通过redo和innodb的存储引擎日志缓冲（Innodb log buffer）来实现的，当开始一个事务的时候，会记录该事务的lsn(log sequence number)号; 当事务执行时，会往InnoDB存储引擎的日志
的日志缓存里面插入事务日志；当事务提交时，必须将存储引擎的日志缓冲写入磁盘（通过innodb_flush_log_at_trx_commit来控制），也就是写数据前，需要先写日志。这种方式称为“预写日志方式”

5、问了MySQL binlog的几种日志录入格式以及区别
(1)、binlog的日志格式的种类和分别
(2)、适用场景；
(3)、结合第一个问题，每一种日志格式在复制中的优劣。
Statement：每一条会修改数据的sql都会记录在binlog中。
优点：不需要记录每一行的变化，减少了binlog日志量，节约了IO，提高性能。(相比row能节约多少性能 与日志量，这个取决于应用的SQL情况，正常同一条记录修改或者插入row格式所产生的日志量还小于Statement产生的日志量，但是考虑到如果带条 件的update操作，以及整表删除，alter表等操作，ROW格式会产生大量日志，因此在考虑是否使用ROW格式日志时应该跟据应用的实际情况，其所 产生的日志量会增加多少，以及带来的IO性能问题。)
缺点：由于记录的只是执行语句，为了这些语句能在slave上正确运行，因此还必须记录每条语句在执行的时候的 一些相关信息，以保证所有语句能在slave得到和在master端执行时候相同 的结果。另外mysql 的复制,像一些特定函数功能，slave可与master上要保持一致会有很多相关问题(如sleep()函数， last_insert_id()，以及user-defined functions(udf)会出现问题).
使用以下函数的语句也无法被复制：
* LOAD_FILE()
* UUID()
* USER()
* FOUND_ROWS()
* SYSDATE() (除非启动时启用了 --sysdate-is-now 选项)
同时在INSERT ...SELECT 会产生比 RBR 更多的行级锁
2.Row:不记录sql语句上下文相关信息，仅保存哪条记录被修改。
优点： binlog中可以不记录执行的sql语句的上下文相关的信息，仅需要记录那一条记录被修改成什么了。所以rowlevel的日志内容会非常清楚的记录下 每一行数据修改的细节。而且不会出现某些特定情况下的存储过程，或function，以及trigger的调用和触发无法被正确复制的问题
缺点:所有的执行的语句当记录到日志中的时候，都将以每行记录的修改来记录，这样可能会产生大量的日志内容,比 如一条update语句，修改多条记录，则binlog中每一条修改都会有记录，这样造成binlog日志量会很大，特别是当执行alter table之类的语句的时候，由于表结构修改，每条记录都发生改变，那么该表每一条记录都会记录到日志中。
3.Mixedlevel: 是以上两种level的混合使用，一般的语句修改使用statment格式保存binlog，如一些函数，statement无法完成主从复制的操作，则 采用row格式保存binlog,MySQL会根据执行的每一条具体的sql语句来区分对待记录的日志形式，也就是在Statement和Row之间选择 一种.新版本的MySQL中队row level模式也被做了优化，并不是所有的修改都会以row level来记录，像遇到表结构变更的时候就会以statement模式来记录。至于update或者delete等修改数据的语句，还是会记录所有行的 变更。

6、问了下MySQL数据库cpu飙升到500%的话他怎么处理？
(1)、没有经验的，可以不问；
(2)、有经验的，问他们的处理思路。
列出所有进程  show processlist  观察所有进程  多秒没有状态变化的(干掉)
查看超时日志或者错误日志 (做了几年开发,一般会是查询以及大批量的插入会导致cpu与i/o上涨,,,,当然不排除网络状态突然断了,,导致一个请求服务器只接受到一半，比如where子句或分页子句没有发送,,当然的一次被坑经历)

7、sql优化
(1)、explain出来的各种item的意义；
select_type 
表示查询中每个select子句的类型
type
表示MySQL在表中找到所需行的方式，又称“访问类型”
possible_keys 
指出MySQL能使用哪个索引在表中找到行，查询涉及到的字段上若存在索引，则该索引将被列出，但不一定被查询使用
key
显示MySQL在查询中实际使用的索引，若没有使用索引，显示为NULL
key_len
表示索引中使用的字节数，可通过该列计算查询中使用的索引的长度
ref
表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值 
Extra
包含不适合在其他列中显示但十分重要的额外信息

(2)、profile的意义以及使用场景；
查询到 SQL 会执行多少时间, 并看出 CPU/Memory 使用量, 执行过程中 Systemlock, Table lock 花多少时间等等

8、备份计划，mysqldump以及xtranbackup的实现原理
(1)、备份计划；
这里每个公司都不一样，您别说那种1小时1全备什么的就行
(2)、备份恢复时间；
这里跟机器，尤其是硬盘的速率有关系，以下列举几个仅供参考
20G的2分钟（mysqldump）
80G的30分钟(mysqldump)
111G的30分钟（mysqldump)
288G的3小时（xtra)
3T的4小时（xtra)
逻辑导入时间一般是备份时间的5倍以上

(3)、xtrabackup实现原理
在InnoDB内部会维护一个redo日志文件，我们也可以叫做事务日志文件。事务日志会存储每一个InnoDB表数据的记录修改。当InnoDB启动时，InnoDB会检查数据文件和事务日志，并执行两个步骤：它应用（前滚）已经提交的事务日志到数据文件，并将修改过但没有提交的数据进行回滚操作。

9、mysqldump中备份出来的sql，如果我想sql文件中，一行只有一个insert....value()的话，怎么办？如果备份需要带上master的复制点信息怎么办？
--skip-extended-insert
[root@helei-zhuanshu ~]# mysqldump -uroot -p helei --skip-extended-insert
Enter password:
  KEY `idx_c1` (`c1`),
  KEY `idx_c2` (`c2`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `helei`
--

LOCK TABLES `helei` WRITE;
/*!40000 ALTER TABLE `helei` DISABLE KEYS */;
INSERT INTO `helei` VALUES (1,32,37,38,'2016-10-18 06:19:24','susususususususususususu');
INSERT INTO `helei` VALUES (2,37,46,21,'2016-10-18 06:19:24','susususususu');
INSERT INTO `helei` VALUES (3,21,5,14,'2016-10-18 06:19:24','susu');

10、500台db，在最快时间之内重启
puppet，dsh

11、innodb的读写参数优化
(1)、读取参数
global buffer pool以及 local buffer；

(2)、写入参数；
innodb_flush_log_at_trx_commit
innodb_buffer_pool_size

(3)、与IO相关的参数；
innodb_write_io_threads = 8
innodb_read_io_threads = 8
innodb_thread_concurrency = 0

(4)、缓存参数以及缓存的适用场景。
query cache/query_cache_type
并不是所有表都适合使用query cache。造成query cache失效的原因主要是相应的table发生了变更
第一个：读操作多的话看看比例，简单来说，如果是用户清单表，或者说是数据比例比较固定，比如说商品列表，是可以打开的，前提是这些库比较集中，数据库中的实务比较小。
第二个：我们“行骗”的时候，比如说我们竞标的时候压测，把query cache打开，还是能收到qps激增的效果，当然前提示前端的连接池什么的都配置一样。大部分情况下如果写入的居多，访问量并不多，那么就不要打开，例如社交网站的，10%的人产生内容，其余的90%都在消费，打开还是效果很好的，但是你如果是qq消息，或者聊天，那就很要命。
第三个：小网站或者没有高并发的无所谓，高并发下，会看到 很多 qcache 锁 等待，所以一般高并发下，不建议打开query cache


12、你是如何监控你们的数据库的？你们的慢日志都是怎么查询的？
监控的工具有很多，例如zabbix，lepus，我这里用的是lepus

13、你是否做过主从一致性校验，如果有，怎么做的，如果没有，你打算怎么做？
主从一致性校验有多种工具 例如checksum、mysqldiff、pt-table-checksum等

14、你们数据库是否支持emoji表情，如果不支持，如何操作？
如果是utf8字符集的话，需要升级至utf8_mb4方可支持

15、你是如何维护数据库的数据字典的？
这个大家维护的方法都不同，我一般是直接在生产库进行注释，利用工具导出成excel方便流通。

16、你们是否有开发规范，如果有，如何执行的
有，开发规范网上有很多了，可以自己看看总结下

17、表中有大字段X(例如：text类型)，且字段X不会经常更新，以读为为主，请问
(1)、您是选择拆成子表，还是继续放一起；
(2)、写出您这样选择的理由。
答：拆带来的问题：连接消耗 + 存储拆分空间；不拆可能带来的问题：查询性能；
如果能容忍拆分带来的空间问题,拆的话最好和经常要查询的表的主键在物理结构上放置在一起(分区) 顺序IO,减少连接消耗,最后这是一个文本列再加上一个全文索引来尽量抵消连接消耗
如果能容忍不拆分带来的查询性能损失的话:上面的方案在某个极致条件下肯定会出现问题,那么不拆就是最好的选择

18、MySQL中InnoDB引擎的行锁是通过加在什么上完成(或称实现)的？为什么是这样子的？
答：InnoDB是基于索引来完成行锁
例: select * from tab_with_index where id = 1 for update;
for update 可以根据条件来完成行锁锁定,并且 id 是有索引键的列,
如果 id 不是索引键那么InnoDB将完成表锁,,并发将无从谈起
.
19、如何从mysqldump产生的全库备份中只恢复某一个库、某一张表？
答案见：http://suifu.blog.51cto.com/9167728/1830651

开放性问题：据说是腾讯的
一个6亿的表a，一个3亿的表b，通过外间tid关联，你如何最快的查询出满足条件的第50000到第50200中的这200条数据记录。
1、如果A表TID是自增长,并且是连续的,B表的ID为索引
select * from a,b where a.tid = b.id and a.tid>500000 limit 200;

2、如果A表的TID不是连续的,那么就需要使用覆盖索引.TID要么是主键,要么是辅助索引,B表ID也需要有索引。
select * from b , (select tid from a limit 50000,200) a where b.id = a .tid;


1. 主键 超键 候选键 外键
主 键：

数据库表中对储存数据对象予以唯一和完整标识的数据列或属性的组合。一个数据列只能有一个主键，且主键的取值不能缺失，即不能为空值（Null）。

超 键：

在关系中能唯一标识元组的属性集称为关系模式的超键。一个属性可以为作为一个超键，多个属性组合在一起也可以作为一个超键。超键包含候选键和主键。

候选键：

是最小超键，即没有冗余元素的超键。

外 键：

在一个表中存在的另一个表的主键称此表的外键。

2.数据库事务的四个特性及含义
数据库事务transanction正确执行的四个基本要素。ACID,原子性(Atomicity)、一致性(Correspondence)、隔离性(Isolation)、持久性(Durability)。
原子性:整个事务中的所有操作，要么全部完成，要么全部不完成，不可能停滞在中间某个环节。事务在执行过程中发生错误，会被回滚（Rollback）到事务开始前的状态，就像这个事务从来没有执行过一样。
一致性:在事务开始之前和事务结束以后，数据库的完整性约束没有被破坏。
隔离性:隔离状态执行事务，使它们好像是系统在给定时间内执行的唯一操作。如果有两个事务，运行在相同的时间内，执行 相同的功能，事务的隔离性将确保每一事务在系统中认为只有该事务在使用系统。这种属性有时称为串行化，为了防止事务操作间的混淆，必须串行化或序列化请 求，使得在同一时间仅有一个请求用于同一数据。
持久性:在事务完成以后，该事务所对数据库所作的更改便持久的保存在数据库之中，并不会被回滚。

3.视图的作用，视图可以更改么？
视图是虚拟的表，与包含数据的表不一样，视图只包含使用时动态检索数据的查询；不包含任何列或数据。使用视图可以简化复杂的sql操作，隐藏具体的细节，保护数据；视图创建后，可以使用与表相同的方式利用它们。
视图不能被索引，也不能有关联的触发器或默认值，如果视图本身内有order by 则对视图再次order by将被覆盖。
创建视图：create view XXX as XXXXXXXXXXXXXX;
对于某些视图比如未使用联结子查询分组聚集函数Distinct Union等，是可以对其更新的，对视图的更新将对基表进行更新；但是视图主要用于简化检索，保护数据，并不用于更新，而且大部分视图都不可以更新。

4.drop,delete与truncate的区别
drop直接删掉表 truncate删除表中数据，再插入时自增长id又从1开始 delete删除表中数据，可以加where字句。

（1） DELETE语句执行删除的过程是每次从表中删除一行，并且同时将该行的删除操作作为事务记录在日志中保存以便进行进行回滚操作。TRUNCATE TABLE 则一次性地从表中删除所有的数据并不把单独的删除操作记录记入日志保存，删除行是不能恢复的。并且在删除的过程中不会激活与表有关的删除触发器。执行速度快。

（2） 表和索引所占空间。当表被TRUNCATE 后，这个表和索引所占用的空间会恢复到初始大小，而DELETE操作不会减少表或索引所占用的空间。drop语句将表所占用的空间全释放掉。

（3） 一般而言，drop > truncate > delete

（4） 应用范围。TRUNCATE 只能对TABLE；DELETE可以是table和view

（5） TRUNCATE 和DELETE只删除数据，而DROP则删除整个表（结构和数据）。

（6） truncate与不带where的delete ：只删除数据，而不删除表的结构（定义）drop语句将删除表的结构被依赖的约束（constrain),触发器（trigger)索引（index);依赖于该表的存储过程/函数将被保留，但其状态会变为：invalid。

（7） delete语句为DML（data maintain Language),这个操作会被放到 rollback segment中,事务提交后才生效。如果有相应的 tigger,执行的时候将被触发。

（8） truncate、drop是DLL（data define language),操作立即生效，原数据不放到 rollback segment中，不能回滚

（9） 在没有备份情况下，谨慎使用 drop 与 truncate。要删除部分数据行采用delete且注意结合where来约束影响范围。回滚段要足够大。要删除表用drop;若想保留表而将表中数据删除，如果于事务无关，用truncate即可实现。如果和事务有关，或老师想触发trigger,还是用delete。

（10） Truncate table 表名 速度快,而且效率高,因为:
truncate table 在功能上与不带 WHERE 子句的 DELETE 语句相同：二者均删除表中的全部行。但 TRUNCATE TABLE 比 DELETE 速度快，且使用的系统和事务日志资源少。DELETE 语句每次删除一行，并在事务日志中为所删除的每行记录一项。TRUNCATE TABLE 通过释放存储表数据所用的数据页来删除数据，并且只在事务日志中记录页的释放。

（11） TRUNCATE TABLE 删除表中的所有行，但表结构及其列、约束、索引等保持不变。新行标识所用的计数值重置为该列的种子。如果想保留标识计数值，请改用 DELETE。如果要删除表定义及其数据，请使用 DROP TABLE 语句。

（12） 对于由 FOREIGN KEY 约束引用的表，不能使用 TRUNCATE TABLE，而应使用不带 WHERE 子句的 DELETE 语句。由于 TRUNCATE TABLE 不记录在日志中，所以它不能激活触发器。

5.索引的工作原理及其种类
数据库索引，是数据库管理系统中一个排序的数据结构，以协助快速查询、更新数据库表中数据。索引的实现通常使用B树及其变种B+树。

在数据之外，数据库系统还维护着满足特定查找算法的数据结构，这些数据结构以某种方式引用（指向）数据，这样就可以在这些数据结构上实现高级查找算法。这种数据结构，就是索引。

为表设置索引要付出代价的：一是增加了数据库的存储空间，二是在插入和修改数据时要花费较多的时间(因为索引也要随之变动)。

\

 

图展示了一种可能的索引方式。左边是数据表，一共有两列七条记录，最左边的是数据记录的物理地址（注意逻辑上相邻的记录在磁盘上也并不是一定物理相邻的）。为了加快Col2的查找，可以维护一个右边所示的二叉查找树，每个节点分别包含索引键值和一个指向对应数据记录物理地址的指针，这样就可以运用二叉查找在O(log2n)的复杂度内获取到相应数据。

创建索引可以大大提高系统的性能。

第一，通过创建唯一性索引，可以保证数据库表中每一行数据的唯一性。

第二，可以大大加快数据的检索速度，这也是创建索引的最主要的原因。

第三，可以加速表和表之间的连接，特别是在实现数据的参考完整性方面特别有意义。

第四，在使用分组和排序子句进行数据检索时，同样可以显著减少查询中分组和排序的时间。

第五，通过使用索引，可以在查询的过程中，使用优化隐藏器，提高系统的性能。

也许会有人要问：增加索引有如此多的优点，为什么不对表中的每一个列创建一个索引呢？因为，增加索引也有许多不利的方面。

第一，创建索引和维护索引要耗费时间，这种时间随着数据量的增加而增加。

第二，索引需要占物理空间，除了数据表占数据空间之外，每一个索引还要占一定的物理空间，如果要建立聚簇索引，那么需要的空间就会更大。

第三，当对表中的数据进行增加、删除和修改的时候，索引也要动态的维护，这样就降低了数据的维护速度。

索引是建立在数据库表中的某些列的上面。在创建索引的时候，应该考虑在哪些列上可以创建索引，在哪些列上不能创建索引。一般来说，应该在这些列上创建索引：在经常需要搜索的列上，可以加快搜索的速度；在作为主键的列上，强制该列的唯一性和组织表中数据的排列结构；在经常用在连接的列上，这些列主要是一些外键，可以加快连接的速度；在经常需要根据范围进行搜索的列上创建索引，因为索引已经排序，其指定的范围是连续的；在经常需要排序的列上创建索引，因为索引已经排序，这样查询可以利用索引的排序，加快排序查询时间；在经常使用在WHERE子句中的列上面创建索引，加快条件的判断速度。

同样，对于有些列不应该创建索引。一般来说，不应该创建索引的的这些列具有下列特点：

第一，对于那些在查询中很少使用或者参考的列不应该创建索引。这是因为，既然这些列很少使用到，因此有索引或者无索引，并不能提高查询速度。相反，由于增加了索引，反而降低了系统的维护速度和增大了空间需求。

第二，对于那些只有很少数据值的列也不应该增加索引。这是因为，由于这些列的取值很少，例如人事表的性别列，在查询的结果中，结果集的数据行占了表中数据行的很大比例，即需要在表中搜索的数据行的比例很大。增加索引，并不能明显加快检索速度。

第三，对于那些定义为text, image和bit数据类型的列不应该增加索引。这是因为，这些列的数据量要么相当大，要么取值很少。

第四，当修改性能远远大于检索性能时，不应该创建索引。这是因为，修改性能和检索性能是互相矛盾的。当增加索引时，会提高检索性能，但是会降低修改性能。当减少索引时，会提高修改性能，降低检索性能。因此，当修改性能远远大于检索性能时，不应该创建索引。

根据数据库的功能，可以在数据库设计器中创建三种索引：唯一索引、主键索引和聚集索引。

唯一索引

唯一索引是不允许其中任何两行具有相同索引值的索引。

当现有数据中存在重复的键值时，大多数数据库不允许将新创建的唯一索引与表一起保存。数据库还可能防止添加将在表中创建重复键值的新数据。例如，如果在employee表中职员的姓(lname)上创建了唯一索引，则任何两个员工都不能同姓。 主键索引 数据库表经常有一列或列组合，其值唯一标识表中的每一行。该列称为表的主键。 在数据库关系图中为表定义主键将自动创建主键索引，主键索引是唯一索引的特定类型。该索引要求主键中的每个值都唯一。当在查询中使用主键索引时，它还允许对数据的快速访问。 聚集索引 在聚集索引中，表中行的物理顺序与键值的逻辑（索引）顺序相同。一个表只能包含一个聚集索引。

如果某索引不是聚集索引，则表中行的物理顺序与键值的逻辑顺序不匹配。与非聚集索引相比，聚集索引通常提供更快的数据访问速度。

局部性原理与磁盘预读
由于存储介质的特性，磁盘本身存取就比主存慢很多，再加上机械运动耗费，磁盘的存取速度往往是主存的几百分分之一，因此为了提高效率，要尽量减少磁盘I/O。为了达到这个目的，磁盘往往不是严格按需读取，而是每次都会预读，即使只需要一个字节，磁盘也会从这个位置开始，顺序向后读取一定长度的数据放入内存。这样做的理论依据是计算机科学中著名的局部性原理：当一个数据被用到时，其附近的数据也通常会马上被使用。程序运行期间所需要的数据通常比较集中。

由于磁盘顺序读取的效率很高（不需要寻道时间，只需很少的旋转时间），因此对于具有局部性的程序来说，预读可以提高I/O效率。

预读的长度一般为页（page）的整倍数。页是计算机管理存储器的逻辑块，硬件及操作系统往往将主存和磁盘存储区分割为连续的大小相等的块，每个存储块称为一页（在许多操作系统中，页得大小通常为4k），主存和磁盘以页为单位交换数据。当程序要读取的数据不在主存中时，会触发一个缺页异常，此时系统会向磁盘发出读盘信号，磁盘会找到数据的起始位置并向后连续读取一页或几页载入内存中，然后异常返回，程序继续运行。

B-/+Tree索引的性能分析
到这里终于可以分析B-/+Tree索引的性能了。

上文说过一般使用磁盘I/O次数评价索引结构的优劣。先从B-Tree分析，根据B-Tree的定义，可知检索一次最多需要访问h个节点。数据库系统的设计者巧妙利用了磁盘预读原理，将一个节点的大小设为等于一个页，这样每个节点只需要一次I/O就可以完全载入。为了达到这个目的，在实际实现B-Tree还需要使用如下技巧：

每次新建节点时，直接申请一个页的空间，这样就保证一个节点物理上也存储在一个页里，加之计算机存储分配都是按页对齐的，就实现了一个node只需一次I/O。

B-Tree中一次检索最多需要h-1次I/O（根节点常驻内存），渐进复杂度为O(h)=O(logdN)。一般实际应用中，出度d是非常大的数字，通常超过100，因此h非常小（通常不超过3）。

而红黑树这种结构，h明显要深的多。由于逻辑上很近的节点（父子）物理上可能很远，无法利用局部性，所以红黑树的I/O渐进复杂度也为O(h)，效率明显比B-Tree差很多。

综上所述，用B-Tree作为索引结构效率是非常高的。

6.连接的种类
查询分析器中执行：
--建表table1,table2：
create table table1(id int,name varchar(10))
create table table2(id int,score int)
insert into table1 select 1,'lee'
insert into table1 select 2,'zhang'
insert into table1 select 4,'wang'
insert into table2 select 1,90
insert into table2 select 2,100
insert into table2 select 3,70
如表
-------------------------------------------------
table1 | table2 |
-------------------------------------------------
id name |id score |
1 lee |1 90|
2 zhang| 2 100|
4 wang| 3 70|
-------------------------------------------------

以下均在查询分析器中执行
一、外连接
1.概念：包括左向外联接、右向外联接或完整外部联接

2.左连接：left join 或 left outer join
(1)左向外联接的结果集包括 LEFT OUTER 子句中指定的左表的所有行，而不仅仅是联接列所匹配的行。如果左表的某行在右表中没有匹配行，则在相关联的结果集行中右表的所有选择列表列均为空值(null)。
(2)sql 语句
select * from table1 left join table2 on table1.id=table2.id
-------------结果-------------
idnameidscore
------------------------------
1lee190
2zhang2100
4wangNULLNULL
------------------------------
注释：包含table1的所有子句，根据指定条件返回table2相应的字段，不符合的以null显示

3.右连接：right join 或 right outer join
(1)右向外联接是左向外联接的反向联接。将返回右表的所有行。如果右表的某行在左表中没有匹配行，则将为左表返回空值。
(2)sql 语句
select * from table1 right join table2 on table1.id=table2.id
-------------结果-------------
idnameidscore
------------------------------
1lee190
2zhang2100
NULLNULL370
------------------------------
注释：包含table2的所有子句，根据指定条件返回table1相应的字段，不符合的以null显示

4.完整外部联接:full join 或 full outer join
(1)完整外部联接返回左表和右表中的所有行。当某行在另一个表中没有匹配行时，则另一个表的选择列表列包含空值。如果表之间有匹配行，则整个结果集行包含基表的数据值。
(2)sql 语句
select * from table1 full join table2 on table1.id=table2.id
-------------结果-------------
idnameidscore
------------------------------
1lee190
2zhang2100
4wangNULLNULL
NULLNULL370
------------------------------
注释：返回左右连接的和（见上左、右连接）

二、内连接
1.概念：内联接是用比较运算符比较要联接列的值的联接

2.内连接：join 或 inner join

3.sql 语句
select * from table1 join table2 on table1.id=table2.id
-------------结果-------------
idnameidscore
------------------------------
1lee190
2zhang2100
------------------------------
注释：只返回符合条件的table1和table2的列

4.等价（与下列执行效果相同）
A:select a.*,b.* from table1 a,table2 b where a.id=b.id
B:select * from table1 cross join table2 where table1.id=table2.id (注：cross join后加条件只能用where,不能用on)

三、交叉连接(完全)

1.概念：没有 WHERE 子句的交叉联接将产生联接所涉及的表的笛卡尔积。第一个表的行数乘以第二个表的行数等于笛卡尔积结果集的大小。（table1和table2交叉连接产生3*3=9条记录）

2.交叉连接：cross join (不带条件where...)

3.sql语句
select * from table1 cross join table2
-------------结果-------------
idnameidscore
------------------------------
1lee190
2zhang190
4wang190
1lee2100
2zhang2100
4wang2100
1lee370
2zhang370
4wang370
------------------------------
注释：返回3*3=9条记录，即笛卡尔积

4.等价（与下列执行效果相同）
A:select * from table1,table2

7.数据库范式
1 第一范式（1NF）

在任何一个关系数据库中，第一范式（1NF）是对关系模式的基本要求，不满足第一范式（1NF）的数据库就不是关系数据库。
所谓第一范式（1NF）是指数据库表的每一列都是不可分割的基本数据项，同一列中不能有多个值，即实体中的某个属性不能有多个值或者不能有重复的属性。如果出现重复的属性，就可能需要定义一个新的实体，新的实体由重复的属性构成，新实体与原实体之间为一对多关系。在第一范式（1NF）中表的每一行只包含一个实例的信息。简而言之，第一范式就是无重复的列。

2 第二范式（2NF）

第二范式（2NF）是在第一范式（1NF）的基础上建立起来的，即满足第二范式（2NF）必须先满足第一范式（1NF）。第二范式（2NF）要求数据库表中的每个实例或行必须可以被惟一地区分。为实现区分通常需要为表加上一个列，以存储各个实例的惟一标识。这个惟一属性列被称为主关键字或主键、主码。
第二范式（2NF）要求实体的属性完全依赖于主关键字。所谓完全依赖是指不能存在仅依赖主关键字一部分的属性，如果存在，那么这个属性和主关键字的这一部分应该分离出来形成一个新的实体，新实体与原实体之间是一对多的关系。为实现区分通常需要为表加上一个列，以存储各个实例的惟一标识。简而言之，第二范式就是非主属性非部分依赖于主关键字。

3 第三范式（3NF）

满足第三范式（3NF）必须先满足第二范式（2NF）。简而言之，第三范式（3NF）要求一个数据库表中不包含已在其它表中已包含的非主关键字信息。例如，存在一个部门信息表，其中每个部门有部门编号（dept_id）、部门名称、部门简介等信息。那么在员工信息表中列出部门编号后就不能再将部门名称、部门简介等与部门有关的信息再加入员工信息表中。如果不存在部门信息表，则根据第三范式（3NF）也应该构建它，否则就会有大量的数据冗余。简而言之，第三范式就是属性不依赖于其它非主属性。（我的理解是消除冗余）

 

8.数据库优化的思路
这个我借鉴了慕课上关于数据库优化的课程。

1.SQL语句优化
1）应尽量避免在 where 子句中使用!=或<>操作符，否则将引擎放弃使用索引而进行全表扫描。
2）应尽量避免在 where 子句中对字段进行 null 值判断，否则将导致引擎放弃使用索引而进行全表扫描，如：
select id from t where num is null
可以在num上设置默认值0，确保表中num列没有null值，然后这样查询：
select id from t where num=0
3）很多时候用 exists 代替 in 是一个好的选择
4）用Where子句替换HAVING 子句 因为HAVING 只会在检索出所有记录之后才对结果集进行过滤

2.索引优化
看上文索引

3.数据库结构优化
1）范式优化： 比如消除冗余（节省空间。。） 2）反范式优化：比如适当加冗余等（减少join） 3）拆分表： 分区将数据在物理上分隔开，不同分区的数据可以制定保存在处于不同磁盘上的数据文件里。这样，当对这个表进行查询时，只需要在表分区中进行扫描，而不必进行全表扫描，明显缩短了查询时间，另外处于不同磁盘的分区也将对这个表的数据传输分散在不同的磁盘I/O，一个精心设置的分区可以将数据传输对磁盘I/O竞争均匀地分散开。对数据量大的时时表可采取此方法。可按月自动建表分区。
4）拆分其实又分垂直拆分和水平拆分： 案例： 简单购物系统暂设涉及如下表： 1.产品表（数据量10w，稳定） 2.订单表（数据量200w，且有增长趋势） 3.用户表 （数据量100w，且有增长趋势） 以mysql为例讲述下水平拆分和垂直拆分，mysql能容忍的数量级在百万静态数据可以到千万 垂直拆分：解决问题：表与表之间的io竞争 不解决问题：单表中数据量增长出现的压力 方案： 把产品表和用户表放到一个server上 订单表单独放到一个server上 水平拆分： 解决问题：单表中数据量增长出现的压力 不解决问题：表与表之间的io争夺
方案： 用户表通过性别拆分为男用户表和女用户表 订单表通过已完成和完成中拆分为已完成订单和未完成订单 产品表 未完成订单放一个server上 已完成订单表盒男用户表放一个server上 女用户表放一个server上(女的爱购物 哈哈)

4.服务器硬件优化
这个么多花钱咯！

9.存储过程与触发器的区别
触发器与存储过程非常相似，触发器也是SQL语句集，两者唯一的区别是触发器不能用EXECUTE语句调用，而是在用户执行Transact-SQL语句时自动触发（激活）执行。触发器是在一个修改了指定表中的数据时执行的存储过程。通常通过创建触发器来强制实现不同表中的逻辑相关数据的引用完整性和一致性。由于用户不能绕过触发器，所以可以用它来强制实施复杂的业务规则，以确保数据的完整性。触发器不同于存储过程，触发器主要是通过事件执行触发而被执行的，而存储过程可以通过存储过程名称名字而直接调用。当对某一表进行诸如UPDATE、INSERT、DELETE这些操作时，SQLSERVER就会自动执行触发器所定义的SQL语句，从而确保对数据的处理必须符合这些SQL语句所定义的规则。

1、MySQL的复制原理以及流程
(1)、复制基本原理流程

1. 主：binlog线程——记录下所有改变了数据库数据的语句，放进master上的binlog中；
2. 从：io线程——在使用start slave 之后，负责从master上拉取 binlog 内容，放进 自己的relay log中；
3. 从：sql执行线程——执行relay log中的语句；
(2)、MySQL复制的线程有几个及之间的关联

MySQL 的复制是基于如下 3 个线程的交互（ 多线程复制里面应该是 4 类线程）：
1. Master 上面的 binlog dump 线程，该线程负责将 master 的 binlog event 传到slave；
2. Slave 上面的 IO 线程，该线程负责接收 Master 传过来的 binlog，并写入 relay log；
3. Slave 上面的 SQL 线程，该线程负责读取 relay log 并执行；
4. 如果是多线程复制，无论是 5.6 库级别的假多线程还是 MariaDB 或者 5.7 的真正的多线程复制， SQL 线程只做 coordinator，只负责把 relay log 中的 binlog读出来然后交给 worker 线程， woker 线程负责具体 binlog event 的执行；
(3)、MySQL如何保证复制过程中数据一致性及减少数据同步延时

一致性主要有以下几个方面：

复制代码
1.在 MySQL5.5 以及之前， slave 的 SQL 线程执行的 relay log 的位置只能保存在文件（ relay-log.info）里面，并且该文件默认每执行 10000 次事务做一次同步到磁盘， 这意味着 slave 意外 crash 重启时， SQL 线程执行到的位置和数据库的数据是不一致的，将导致复制报错，如果不重搭复制，则有可能会
导致数据不一致。 MySQL 5.6 引入参数 relay_log_info_repository，将该参数设置为 TABLE 时， MySQL 将 SQL 线程执行到的位置存到mysql.slave_relay_log_info 表，这样更新该表的位置和 SQL 线程执行的用户事务绑定成一个事务，这样 slave 意外宕机后， slave 通过 innodb 的崩溃
恢复可以把 SQL 线程执行到的位置和用户事务恢复到一致性的状态。
2. MySQL 5.6 引入 GTID 复制，每个 GTID 对应的事务在每个实例上面最多执行一次， 这极大地提高了复制的数据一致性；
3. MySQL 5.5 引入半同步复制， 用户安装半同步复制插件并且开启参数后，设置超时时间，可保证在超时时间内如果 binlog 不传到 slave 上面，那么用户提交事务时不会返回，直到超时后切成异步复制，但是如果切成异步之前用户线程提交时在 master 上面等待的时候，事务已经提交，该事务对 master
上面的其他 session 是可见的，如果这时 master 宕机，那么到 slave 上面该事务又不可见了，该问题直到 5.7 才解决；
4. MySQL 5.7 引入无损半同步复制，引入参 rpl_semi_sync_master_wait_point，该参数默认为 after_sync，指的是在切成半同步之前，事务不提交，而是接收到 slave 的 ACK 确认之后才提交该事务，从此，复制真正可以做到无损的了。
5.可以再说一下 5.7 的无损复制情况下， master 意外宕机，重启后发现有 binlog没传到 slave 上面，这部分 binlog 怎么办？？？分 2 种情况讨论， 1 宕机时已经切成异步了， 2 是宕机时还没切成异步？？？ 这个怎么判断宕机时有没有切成异步呢？？？ 分别怎么处理？？？
复制代码
延时性：

 5.5 是单线程复制， 5.6 是多库复制（对于单库或者单表的并发操作是没用的）， 5.7 是真正意义的多线程复制，它的原理是基于 group commit， 只要
master 上面的事务是 group commit 的，那 slave 上面也可以通过多个 worker线程去并发执行。 和 MairaDB10.0.0.5 引入多线程复制的原理基本一样。
(4)、工作遇到的复制 bug 的解决方法

5.6 的多库复制有时候自己会停止，我们写了一个脚本重新 start slave;待补充…
 

2、MySQL中myisam与innodb的区别，至少5点
(1)、问5点不同

复制代码
1.InnoDB支持事物，而MyISAM不支持事物
2.InnoDB支持行级锁，而MyISAM支持表级锁
3.InnoDB支持MVCC, 而MyISAM不支持
4.InnoDB支持外键，而MyISAM不支持
5.InnoDB不支持全文索引，而MyISAM支持。
6.InnoDB不能通过直接拷贝表文件的方法拷贝表到另外一台机器， myisam 支持
7.InnoDB表支持多种行格式， myisam 不支持
8.InnoDB是索引组织表， myisam 是堆表
复制代码
(2)、innodb引擎的4大特性

1.插入缓冲（insert buffer)
2.二次写(double write)
3.自适应哈希索引(ahi)
4.预读(read ahead)
(3)、各种不同 mysql 版本的Innodb的改进

复制代码
MySQL5.6 下 Innodb 引擎的主要改进：
（ 1） online DDL
（ 2） memcached NoSQL 接口
（ 3） transportable tablespace（ alter table discard/import tablespace）
（ 4） MySQL 正常关闭时，可以 dump 出 buffer pool 的（ space， page_no），重启时 reload，加快预热速度
（ 5） 索引和表的统计信息持久化到 mysql.innodb_table_stats 和mysql.innodb_index_stats，可提供稳定的执行计划
（ 6） Compressed row format 支持压缩表

MySQL 5.7 innodb 引擎主要改进
（ 1） 修改 varchar 字段长度有时可以使用 online DDL
（ 2） Buffer pool 支持在线改变大小
（ 3） Buffer pool 支持导出部分比例
（ 4） 支持新建 innodb tablespace，并可以在其中创建多张表
（ 5） 磁盘临时表采用 innodb 存储，并且存储在 innodb temp tablespace 里面，以前是 myisam 存储
（ 6） 透明表空间压缩功能
复制代码
(4)、2者select  count(*)哪个更快，为什么

myisam更快，因为myisam内部维护了一个计数器，可以直接调取。
(5)、2 者的索引的实现方式

都是 B+树索引， Innodb 是索引组织表， myisam 是堆表， 索引组织表和堆表的区别要熟悉
 

3、MySQL中varchar与char的区别以及varchar(50)中的50代表的涵义
(1)、varchar与char的区别

在单字节字符集下， char（ N） 在内部存储的时候总是定长， 而且没有变长字段长度列表中。 在多字节字符集下面， char(N)如果存储的字节数超过 N，那么 char（ N）将和 varchar（ N）没有区别。在多字节字符集下面，如果存
储的字节数少于 N，那么存储 N 个字节，后面补空格，补到 N 字节长度。 都存储变长的数据和变长字段长度列表。 varchar(N)无论是什么字节字符集，都是变长的，即都存储变长数据和变长字段长度列表。
(2)、varchar(50)中50的涵义

最多存放50个字符，varchar(50)和(200)存储hello所占空间一样，但后者在排序时会消耗更多内存，因为order by col采用fixed_length计算col长度(memory引擎也一样)。在早期 MySQL 版本中， 50 代表字节数，现在代表字符数。
(3)、int（20）中20的涵义

是指显示字符的长度
不影响内部存储，只是影响带 zerofill 定义的 int 时，前面补多少个 0，易于报表展示
(4)、mysql为什么这么设计

对大多数应用没有意义，只是规定一些工具用来显示字符的个数；int(1)和int(20)存储和计算均一样；
 

4、innodb的事务与日志的实现方式
(1)、有多少种日志

redo和undo
(2)、日志的存放形式

redo：在页修改的时候，先写到 redo log buffer 里面， 然后写到 redo log 的文件系统缓存里面(fwrite)，然后再同步到磁盘文件（ fsync）。
Undo：在 MySQL5.5 之前， undo 只能存放在 ibdata*文件里面， 5.6 之后，可以通过设置 innodb_undo_tablespaces 参数把 undo log 存放在 ibdata*之外。
(3)、事务是如何通过日志来实现的，说得越深入越好

基本流程如下：
因为事务在修改页时，要先记 undo，在记 undo 之前要记 undo 的 redo， 然后修改数据页，再记数据页修改的 redo。 Redo（里面包括 undo 的修改） 一定要比数据页先持久化到磁盘。 当事务需要回滚时，因为有 undo，可以把数据页回滚到前镜像的
状态，崩溃恢复时，如果 redo log 中事务没有对应的 commit 记录，那么需要用 undo把该事务的修改回滚到事务开始之前。 如果有 commit 记录，就用 redo 前滚到该事务完成时并提交掉。
 

5、MySQL binlog的几种日志录入格式以及区别
(1)、 各种日志格式的涵义

复制代码
1.Statement：每一条会修改数据的sql都会记录在binlog中。
优点：不需要记录每一行的变化，减少了binlog日志量，节约了IO，提高性能。(相比row能节约多少性能 与日志量，这个取决于应用的SQL情况，正常同一条记录修改或者插入row格式所产生的日志量还小于Statement产生的日志量，
但是考虑到如果带条 件的update操作，以及整表删除，alter表等操作，ROW格式会产生大量日志，因此在考虑是否使用ROW格式日志时应该跟据应用的实际情况，其所 产生的日志量会增加多少，以及带来的IO性能问题。)
缺点：由于记录的只是执行语句，为了这些语句能在slave上正确运行，因此还必须记录每条语句在执行的时候的 一些相关信息，以保证所有语句能在slave得到和在master端执行时候相同 的结果。另外mysql 的复制,
像一些特定函数功能，slave可与master上要保持一致会有很多相关问题(如sleep()函数， last_insert_id()，以及user-defined functions(udf)会出现问题).
使用以下函数的语句也无法被复制：
* LOAD_FILE()
* UUID()
* USER()
* FOUND_ROWS()
* SYSDATE() (除非启动时启用了 --sysdate-is-now 选项)
同时在INSERT ...SELECT 会产生比 RBR 更多的行级锁

2.Row:不记录sql语句上下文相关信息，仅保存哪条记录被修改。
优点： binlog中可以不记录执行的sql语句的上下文相关的信息，仅需要记录那一条记录被修改成什么了。所以rowlevel的日志内容会非常清楚的记录下 每一行数据修改的细节。而且不会出现某些特定情况下的存储过程，或function，以及trigger的调用和触发无法被正确复制的问题
缺点:所有的执行的语句当记录到日志中的时候，都将以每行记录的修改来记录，这样可能会产生大量的日志内容,比 如一条update语句，修改多条记录，则binlog中每一条修改都会有记录，这样造成binlog日志量会很大，特别是当执行alter table之类的语句的时候，
由于表结构修改，每条记录都发生改变，那么该表每一条记录都会记录到日志中。

3.Mixedlevel: 是以上两种level的混合使用，一般的语句修改使用statment格式保存binlog，如一些函数，statement无法完成主从复制的操作，则 采用row格式保存binlog,MySQL会根据执行的每一条具体的sql语句来区分对待记录的日志形式，
也就是在Statement和Row之间选择 一种.新版本的MySQL中队row level模式也被做了优化，并不是所有的修改都会以row level来记录，像遇到表结构变更的时候就会以statement模式来记录。至于update或者delete等修改数据的语句，还是会记录所有行的变更。
复制代码
 (2)、适用场景

在一条 SQL 操作了多行数据时， statement 更节省空间， row 更占用空间。但是 row模式更可靠。
(3)、结合第一个问题，每一种日志格式在复制中的优劣

Statement 可能占用空间会相对小一些，传送到 slave 的时间可能也短，但是没有 row模式的可靠。 Row 模式在操作多行数据时更占用空间， 但是可靠。
 

6、下MySQL数据库cpu飙升到500%的话他怎么处理？
当 cpu 飙升到 500%时，先用操作系统命令 top 命令观察是不是 mysqld 占用导致的，如果不是，找出占用高的进程，并进行相关处理。如果是 mysqld 造成的， show processlist，看看里面跑的 session 情况，是不是有消耗资源的 sql 在运行。找出消耗高的 sql，
看看执行计划是否准确， index 是否缺失，或者实在是数据量太大造成。一般来说，肯定要 kill 掉这些线程(同时观察 cpu 使用率是否下降)，等进行相应的调整(比如说加索引、改 sql、改内存参数)之后，再重新跑这些 SQL。也有可能是每个 sql 消耗资源并不多，但是突然之间，
有大量的 session 连进来导致 cpu 飙升，这种情况就需要跟应用一起来分析为何连接数会激增，再做出相应的调整，比如说限制连接数等
 

7、sql优化
(1)、explain出来的各种item的意义

复制代码
id:每个被独立执行的操作的标志，表示对象被操作的顺序。一般来说， id 值大，先被执行；如果 id 值相同，则顺序从上到下。
select_type：查询中每个 select 子句的类型。
table:名字，被操作的对象名称，通常的表名(或者别名)，但是也有其他格式。
partitions:匹配的分区信息。
type:join 类型。
possible_keys：列出可能会用到的索引。
key:实际用到的索引。
key_len:用到的索引键的平均长度，单位为字节。
ref:表示本行被操作的对象的参照对象，可能是一个常量用 const 表示，也可能是其他表的
key 指向的对象，比如说驱动表的连接列。
rows:估计每次需要扫描的行数。
filtered:rows*filtered/100 表示该步骤最后得到的行数(估计值)。
extra:重要的补充信息。
复制代码
(2)、profile的意义以及使用场景

Profile 用来分析 sql 性能的消耗分布情况。当用 explain 无法解决慢 SQL 的时候，需要用profile 来对 sql 进行更细致的分析，找出 sql 所花的时间大部分消耗在哪个部分，确认 sql的性能瓶颈。
(3)、explain 中的索引问题

Explain 结果中，一般来说，要看到尽量用 index(type 为 const、 ref 等， key 列有值)，避免使用全表扫描(type 显式为 ALL)。比如说有 where 条件且选择性不错的列，需要建立索引。
被驱动表的连接列，也需要建立索引。被驱动表的连接列也可能会跟 where 条件列一起建立联合索引。当有排序或者 group by 的需求时，也可以考虑建立索引来达到直接排序和汇总的需求。
 

8、备份计划，mysqldump以及xtranbackup的实现原理
(1)、备份计划

视库的大小来定，一般来说 100G 内的库，可以考虑使用 mysqldump 来做，因为 mysqldump更加轻巧灵活，备份时间选在业务低峰期，可以每天进行都进行全量备份(mysqldump 备份
出来的文件比较小，压缩之后更小)。100G 以上的库，可以考虑用 xtranbackup 来做，备份速度明显要比 mysqldump 要快。一般是选择一周一个全备，其余每天进行增量备份，备份时间为业务低峰期。
(2)、备份恢复时间

复制代码
物理备份恢复快，逻辑备份恢复慢
这里跟机器，尤其是硬盘的速率有关系，以下列举几个仅供参考
20G的2分钟（mysqldump）
80G的30分钟(mysqldump)
111G的30分钟（mysqldump)
288G的3小时（xtra)
3T的4小时（xtra)
逻辑导入时间一般是备份时间的5倍以上
复制代码
(3)、备份恢复失败如何处理

首先在恢复之前就应该做足准备工作，避免恢复的时候出错。比如说备份之后的有效性检查、权限检查、空间检查等。如果万一报错，再根据报错的提示来进行相应的调整。
(4)、mysqldump和xtrabackup实现原理

mysqldump

mysqldump 属于逻辑备份。加入--single-transaction 选项可以进行一致性备份。后台进程会先设置 session 的事务隔离级别为 RR(SET SESSION TRANSACTION ISOLATION LEVELREPEATABLE READ)，
之后显式开启一个事务(START TRANSACTION /*!40100 WITH CONSISTENTSNAPSHOT */)，这样就保证了该事务里读到的数据都是事务事务时候的快照。之后再把表的数据读取出来。 如果加上--master-data=1 的话，在刚开始的时候还会加一个数据库的读锁
(FLUSH TABLES WITH READ LOCK),等开启事务后，再记录下数据库此时 binlog 的位置(showmaster status)，马上解锁，再读取表的数据。等所有的数据都已经导完，就可以结束事务
Xtrabackup:

xtrabackup 属于物理备份，直接拷贝表空间文件，同时不断扫描产生的 redo 日志并保存下来。最后完成 innodb 的备份后，会做一个 flush engine logs 的操作(老版本在有 bug，在5.6 上不做此操作会丢数据)，确保所有的 redo log 都已经落盘(涉及到事务的两阶段提交
概念，因为 xtrabackup 并不拷贝 binlog，所以必须保证所有的 redo log 都落盘，否则可能会丢最后一组提交事务的数据)。这个时间点就是 innodb 完成备份的时间点，数据文件虽然不是一致性的，但是有这段时间的 redo 就可以让数据文件达到一致性(恢复的时候做的事
情)。然后还需要 flush tables with read lock，把 myisam 等其他引擎的表给备份出来，备份完后解锁。 这样就做到了完美的热备。
 

9、mysqldump中备份出来的sql，如果我想sql文件中，一行只有一个insert....value()的话，怎么办？如果备份需要带上master的复制点信息怎么办？
复制代码
--skip-extended-insert
[root@helei-zhuanshu ~]# mysqldump -uroot -p helei --skip-extended-insert
Enter password:
  KEY `idx_c1` (`c1`),
  KEY `idx_c2` (`c2`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `helei`
--

LOCK TABLES `helei` WRITE;
/*!40000 ALTER TABLE `helei` DISABLE KEYS */;
INSERT INTO `helei` VALUES (1,32,37,38,'2016-10-18 06:19:24','susususususususususususu');
INSERT INTO `helei` VALUES (2,37,46,21,'2016-10-18 06:19:24','susususususu');
INSERT INTO `helei` VALUES (3,21,5,14,'2016-10-18 06:19:24','susu');
复制代码
 

10、500台db，在最快时间之内重启
可以使用批量 ssh 工具 pssh 来对需要重启的机器执行重启命令。 也可以使用 salt（前提是客户端有安装 salt）或者 ansible（ ansible 只需要 ssh 免登通了就行）等多线程工具同时操作多台服务器
 

11、innodb的读写参数优化
(1)、读取参数

复制代码
global buffer 以及 local buffer；

Global buffer：
Innodb_buffer_pool_size
innodb_log_buffer_size
innodb_additional_mem_pool_size

local buffer(下面的都是 server 层的 session 变量，不是 innodb 的)：
Read_buffer_size
Join_buffer_size
Sort_buffer_size
Key_buffer_size
Binlog_cache_size
复制代码
(2)、写入参数

innodb_flush_log_at_trx_commit
innodb_buffer_pool_size
insert_buffer_size
innodb_double_write
innodb_write_io_thread
innodb_flush_method
(3)、与IO相关的参数

复制代码
innodb_write_io_threads = 8
innodb_read_io_threads = 8
innodb_thread_concurrency = 0
Sync_binlog
Innodb_flush_log_at_trx_commit
Innodb_lru_scan_depth
Innodb_io_capacity
Innodb_io_capacity_max
innodb_log_buffer_size
innodb_max_dirty_pages_pct
复制代码
(4)、缓存参数以及缓存的适用场景

query cache/query_cache_type
并不是所有表都适合使用query cache。造成query cache失效的原因主要是相应的table发生了变更
第一个：读操作多的话看看比例，简单来说，如果是用户清单表，或者说是数据比例比较固定，比如说商品列表，是可以打开的，前提是这些库比较集中，数据库中的实务比较小。
第二个：我们“行骗”的时候，比如说我们竞标的时候压测，把query cache打开，还是能收到qps激增的效果，当然前提示前端的连接池什么的都配置一样。大部分情况下如果写入的居多，访问量并不多，那么就不要打开，例如社交网站的，10%的人产生内容，其余的90%都在消费，打开还是效果很好的，但是你如果是qq消息，或者聊天，那就很要命。
第三个：小网站或者没有高并发的无所谓，高并发下，会看到 很多 qcache 锁 等待，所以一般高并发下，不建议打开query cache
 

12、你是如何监控你们的数据库的？你们的慢日志都是怎么查询的？
监控的工具有很多，例如zabbix，lepus，我这里用的是lepus
 

13、你是否做过主从一致性校验，如果有，怎么做的，如果没有，你打算怎么做？
主从一致性校验有多种工具 例如checksum、mysqldiff、pt-table-checksum等
 

14、表中有大字段X(例如：text类型)，且字段X不会经常更新，以读为为主，请问您是选择拆成子表，还是继续放一起?写出您这样选择的理由
答：拆带来的问题：连接消耗 + 存储拆分空间；不拆可能带来的问题：查询性能；
如果能容忍拆分带来的空间问题,拆的话最好和经常要查询的表的主键在物理结构上放置在一起(分区) 顺序IO,减少连接消耗,最后这是一个文本列再加上一个全文索引来尽量抵消连接消耗
如果能容忍不拆分带来的查询性能损失的话:上面的方案在某个极致条件下肯定会出现问题,那么不拆就是最好的选择
 

15、MySQL中InnoDB引擎的行锁是通过加在什么上完成(或称实现)的？为什么是这样子的？
答：InnoDB是基于索引来完成行锁
例: select * from tab_with_index where id = 1 for update;
for update 可以根据条件来完成行锁锁定,并且 id 是有索引键的列,
如果 id 不是索引键那么InnoDB将完成表锁,,并发将无从谈起
 

16、如何从mysqldump产生的全库备份中只恢复某一个库、某一张表？
复制代码
全库备份
[root@HE1 ~]# mysqldump -uroot -p --single-transaction -A --master-data=2 >dump.sql
只还原erp库的内容
[root@HE1 ~]# mysql -uroot -pMANAGER erp --one-database <dump.sql

可以看出这里主要用到的参数是--one-database简写-o的参数，极大方便了我们的恢复灵活性
那么如何从全库备份中抽取某张表呢，全库恢复，再恢复某张表小库还可以，大库就很麻烦了，那我们可以利用正则表达式来进行快速抽取，具体实现方法如下：
 
从全库备份中抽取出t表的表结构
[root@HE1 ~]# sed -e'/./{H;$!d;}' -e 'x;/CREATE TABLE `t`/!d;q' dump.sql
 
DROP TABLE IF EXISTS`t`;
/*!40101 SET@saved_cs_client     =@@character_set_client */;
/*!40101 SETcharacter_set_client = utf8 */;
CREATE TABLE `t` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `age` tinyint(4) NOT NULL DEFAULT '0',
  `name` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDBAUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SETcharacter_set_client = @saved_cs_client */;
 
从全库备份中抽取出t表的内容
[root@HE1 ~]# grep'INSERT INTO `t`' dump.sql
INSERT INTO `t`VALUES (0,0,''),(1,0,'aa'),(2,0,'bbb'),(3,25,'helei');
复制代码
 

17、在当前的工作中，你碰到到的最大的 mysql db 问题以及如何解决的？
可以选择一个处理过的比较棘手的案例，或者选择一个老师在课程上讲过的死锁的案例;没有及时 Purge + insert 唯一索引造成的死锁：具体案例可以参考学委笔记。
 

18、请简洁地描述下 MySQL 中 InnoDB 支持的四种事务隔离级别名称，以及逐级之间的区别？
(1)、事物的4种隔离级别

读未提交(read uncommitted)
读已提交(read committed)
可重复读(repeatable read)
串行(serializable)
(2)、不同级别的现象

Read Uncommitted:可以读取其他 session 未提交的脏数据。
Read Committed:允许不可重复读取，但不允许脏读取。提交后，其他会话可以看到提交的数据。
Repeatable Read: 禁止不可重复读取和脏读取、以及幻读(innodb 独有)。
Serializable: 事务只能一个接着一个地执行，但不能并发执行。事务隔离级别最高。
不同的隔离级别有不同的现象，并有不同的锁定/并发机制，隔离级别越高，数据库的并发性就越差。


 

 

面试中其他的问题：
1、2 年 MySQL DBA 经验
复制代码
其中许多有水分，一看到简历自我介绍，说公司项目的时候，会写上 linux 系统维护，mssql server 项目，或者 oracle data gard 项目，一般如果有这些的话，工作在 3 年到 4年的话，他的 2 年 MySQL DBA 管理经验，是有很大的水分的。刚开始我跟领导说，这些
不用去面试了，肯定 mysql dba 经验不足，领导说先面面看看，于是我就面了，结果很多人卡在基础知识这一环节之上，比如：
（ 1）有的卡在复制原理之上
（ 2）有的卡在 binlog 的日志格式的种类和分别
（ 3）有的卡在 innodb 事务与日志的实现上。
（ 4）有的卡在 innodb 与 myisam 的索引实现方式的理解上面。
.........
个人觉得如果有过真正的 2 年 mysql 专职 dba 经验，那么肯定会在 mysql 的基本原理上有所研究，因为很多问题都不得不让你去仔细研究各种细节，而自 己研究过的细节肯定会记忆深刻，别人问起一定会说的头头是道，起码一些最基本的关键参数比如
Seconds_Behind_Master 为 60 这个值 60 的准确涵义，面试了 10+的 mysql dba，没有一个说的准确，有的说不知道忘记了，有的说是差了 60 秒，有的说是与主上执行时间延后了 60 秒。
复制代码
 
2 、对于简历中写有熟悉 mysql 高可用方案
我一般先问他现在管理的数据库架构是什么，如果他只说出了主从，而没有说任何 ha的方案，那么我就可以判断出他没有实际的 ha 经验。不过这时候也不能就是 断定他不懂mysql 高可用，也许是没有实际机会去使用，那么我就要问 mmm 以及 mha 以及mm+keepalived 等的原理
实现方式以及它们之间的优 势和不足了，一般这种情况下，能说出这个的基本没有。mmm 那东西好像不靠谱，据说不稳定，但是有人在用的，我只在虚拟机上面用过，和mysql-router 比较像，都是指定可写的机器和只读机器。 MHA 的话一句话说不完，可以翻翻学委的笔记
 
3 、对于简历中写有批量 MySQL 数据库服务器的管理经验
这个如果他说有的话，我会先问他们现在实际线上的 mysql 数据库数量有多少，分多少个节点组，最后问这些节点组上面的 slow log 是如何组合在一起来统计分析的。如果这些他都答对了，那么我还有一问，就是现在手上有 600 台数据库，新来的机器， Mysql 都
安装好了，那么你如 何在最快的时间里面把这 600 台 mysql 数据库的 mysqld 服务启动起来。这个重点在于最快的时间，而能准确回答出清晰思路的只有 2 个人。slow log 分析：可以通过一个管理服务器定时去各台 MySQL 服务器上面 mv 并且 cp slowlog，
然后分析入库，页面展示。最快的时间里面启动 600 台服务器： 肯定是多线程。 可以用 pssh， ansible 等多线程批量管理服务器的工具
 
4 、对于有丰富的 SQL 优化的经验
首先问 mysql 中 sql 优化的思路，如果能准备说出来， ok，那么我就开始问 explain的各种参数了，重点是 select_type， type， possible_key, ref,rows,extra 等参数的各种
值的含义，如果他都回答正确了，那么我再问 file sort 的含义以及什么时候会出现这个分析结果，如果这里他也回答对了，那么我就准备问 profile 分析了，如果这里他也答对了，那么我就会再问一个问 题，
那是曾经 tx 问我的让我郁闷不已的问题，一个 6 亿的表 a，一个 3 亿的表 b，通过外间 tid 关联，你如何最快的查询出满足条件的第 50000 到第 50200中的这 200 条数据记录。
Explain 在上面的题目中有了，这里就不说了。如何最快的查询出满足条件的第 50000 到第 50200 中的这 200 条数据记录？这个我想不出来！
关于 explain 的各种参数，请参考： http://blog.csdn.net/mchdba/article/details/9190771
 
5、对于有丰富的数据库设计经验
这个对于数据库设计我真的没有太多的经验，我也就只能问问最基础的， mysql 中varchar(60) 60 是啥含义， int(30)中 30 是啥含义？ 如果他都回答对了，那么我就问 mysql中为什么要这么设计呢？
如果他还回答对了，我就继续问 int(20)存储的数字的上限和下限是多少？这个问题难道了全部的 mysql dba 的应聘者，不得不佩服提出这个问题的金总的睿智啊，因为这个问题回答正确了，
那么他确实认认真真地研究了 mysql 的设计中关于字段类型的细节。至 于丰富的设计数据库的经验，不用着急，这不我上面还有更加厉害的 dba吗，他会搞明白的，那就跟我无关了。
varchar(60)的 60 表示最多可以存储 60 个字符。int(30)的 30 表示客户端显示这个字段的宽度。
为何这么设计？说不清楚，请大家补充 。 int(20)的上限为 2147483647(signed)或者4294967295(unsigned)。
 
6 、关于 mysql 参数优化的经验
复制代码
首先问他它们线上 mysql 数据库是怎么安装的，如果说是 rpm 安装的，那么我就直接问调优参数了，如果是源码安装的，那么我就要问编译中的一些参数了，比如 my.cnf 以及存储引擎以及字符类型等等。然后从以下几个方面问起：
（ 1） mysql 有哪些 global 内存参数，有哪些 local 内存参数。
Global:
innodb_buffer_pool_size/innodb_additional_mem_pool_size/innodb_log_buffer_size/key_buffer_size/query_cache_size/table_open_cache/table_definition_cache/thread_cache_size
Local:
read_buffer_size/read_rnd_buffer_size/sort_buffer_size/join_buffer_size/binlog_cache_size/tmp_table_size/thread_stack/bulk_insert_buffer_size

（ 2） mysql 的写入参数需要调整哪些？重要的几个写参数的几个值得含义以及适用场景，
比如 innodb_flush_log_at_trx_commit 等。 (求补充)
sync_binlog 设置为 1，保证 binlog 的安全性。
innodb_flush_log_at_trx_commit：
0：事务提交时不将 redo log buffer 写入磁盘(仅每秒进行 master thread 刷新，安全
性最差，性能最好)
1：事务提交时将 redo log buffer 写入磁盘(安全性最好，性能最差， 推荐生产使用)
2：事务提交时仅将 redo log buffer 写入操作系统缓存(安全性和性能都居中，当 mysql宕机但是操作系统不宕机则不丢数据，如果操作系统宕机，最多丢一秒数据)
innodb_io_capacity/innodb_io_capacity_max：看磁盘的性能来定。如果是 HDD 可以设置为 200-几百不等。如果是 SSD，推荐为 4000 左右。 innodb_io_capacity_max 更大一些。
innodb_flush_method 设置为 O_DIRECT。

（ 3） 读取的话，那几个全局的 pool 的值的设置，以及几个 local 的 buffer 的设置。
Global:
innodb_buffer_pool_size:设置为可用内存的 50%-60%左右，如果不够，再慢慢上调。
innodb_additional_mem_pool_size：采用默认值 8M 即可。
innodb_log_buffer_size:默认值 8M 即可。
key_buffer_size:myisam 表需要的 buffer size，选择基本都用 innodb，所以采用默认的 8M 即可。
Local:
join_buffer_size： 当 sql 有 BNL 和 BKA 的时候，需要用的 buffer_size(plain index
scans, range index scans 的时候可能也会用到)。默认为 256k，建议设置为 16M-32M。
read_rnd_buffer_size：当使用 mrr 时，用到的 buffer。默认为 256k，建议设置为16-32M。
read_buffer_size:当顺序扫描一个 myisam 表，需要用到这个 buffer。或者用来决定memory table 的大小。或者所有的 engine 类型做如下操作：order by 的时候用 temporaryfile、 SELECT INTO … OUTFILE 'filename' 、 For caching results of nested queries。默认为 128K，建议为 16M。
sort_buffer_size： sql 语句用来进行 sort 操作(order by,group by)的 buffer。如果 buffer 不够，则需要建立 temporary file。如果在 show global status 中发现有大量的 Sort_merge_passes 值，则需要考虑调大 sort_buffer_size。默认为 256k，建议设置为 16-32M。
binlog_cache_size： 表示每个 session 中存放 transaction 的 binlog 的 cache size。默认 32K。一般使用默认值即可。如果有大事务，可以考虑调大。
thread_stack： 每个进程都需要有，默认为 256K，使用默认值即可。

（ 4） 还有就是著名的 query cache 了，以及 query cache 的适用场景了，这里有一个陷阱，
就是高并发的情况下，比如双十一的时候， query cache 开还是不开，开了怎么保证高并发，不开又有何别的考虑？建议关闭，上了性能反而更差。
复制代码
 
7、关于熟悉 mysql 的锁机制
gap 锁， next-key 锁，以及 innodb 的行锁是怎么实现的，以及 myisam 的锁是怎么实现的等
Innodb 的锁的策略为 next-key 锁，即 record lock+gap lock。是通过在 index 上加 lock 实现的，如果 index 为 unique index，则降级为 record lock,如果是普通 index，则为 next-key lock，如果没有 index，则直接锁住全表。 myisam 直接使用全表扫描。
 
8、 关于熟悉 mysql 集群的
我就问了 ndbd 的节点的启动先后顺序，再问配置参数中的内存配置几个重要的参数，再问 sql 节点中执行一个 join 表的 select 语句的实现流程是怎么走的？ ok，能回答的也只有一个。
关于 mysql 集群入门资料，请参考： http://write.blog.csdn.net/postlist/1583151/all
 
9、 关于有丰富的备份经验的
复制代码
就问 mysqldump 中备份出来的 sql，如果我想 sql 文件中，一行只有一个 insert .... value()的话，怎么办？如果备份需要带上 master 的复制点信息怎么办？或者 xtrabackup 中如何
做到实时在线备份的？以及 xtrabackup 是如何做到带上 master 的复制点的信息的？ 当前 xtrabackup 做增量备份的时候有何缺陷？能全部回答出来的没有一个，不过没有关系，只要回答出 mysqldump 或者xtrabackup 其中一个的也可以。
1). --skip-extended-insert
2). --master-date=1
3). 因为 xtrabackup 是多线程，一个线程不停地在拷贝新产生的 redo 文件，另外的线程去备份数据库，当所有表空间备份完成的时候，它会执行 flush table with read lock 操作
锁住所有表，然后执行 show master status; 接着执行 flush engine logs; 最后解锁表。执行 show master status; 时就能获取到 mster 的复制点信息，执行 flush engine logs 强制把redo 文件刷新到磁盘。
4). xtrabackup 增量备份的缺陷不了解，在线上用 xtrabackup 备份没有发现什么缺陷。
复制代码
 
10 、关于有丰富的线上恢复经验的
就问你现在线上数据量有多大，如果是 100G，你用 mysqldump 出来要多久，然后 mysql进去又要多久，如果互联网不允许延时的话，你又怎么做到 恢复单张表的时候保证 nagios不报警。如果有人说 mysqldump 出来 1 个小时就 ok 了，那么我就要问问他 db 服务器是
啥配置了，如果他说 mysql 进去 50 分钟搞定了，那么我也要问问他 db 机器啥配置了，如果是普通的吊丝 pc server，那么真实性，大家懂得。然后如果你用 xtrabackup 备份要多久，恢复要多久，大家都知道 copy-back 这一步要很久，那么你有没有办法对这一块优化。
```