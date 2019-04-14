```
Oracle面试题(基础篇)
1. Oracle跟SQL Server 2005的区别？ 
宏观上： 
1). 最大的区别在于平台，oracle可以运行在不同的平台上，sql server只能运行在windows平台上，由于windows平台的稳定性和安全性影响了sql server的稳定性和安全性 
2). oracle使用的脚本语言为PL-SQL，而sql server使用的脚本为T-SQL 
微观上： 从数据类型,数据库的结构等等回答

2. 如何使用Oracle的游标？ 
1).  oracle中的游标分为显示游标和隐式游标 
2).  显示游标是用cursor...is命令定义的游标，它可以对查询语句(select)返回的多条记录进行处理；隐式游标是在执行插入 (insert)、删除(delete)、修改(update)和返回单条记录的查询(select)语句时由PL/SQL自动定义的。 
3). 显式游标的操作：打开游标、操作游标、关闭游标；PL/SQL隐式地打开SQL游标，并在它内部处理SQL语句，然后关闭它

3. Oracle中function和procedure的区别？ 
1). 可以理解函数是存储过程的一种 
2). 函数可以没有参数,但是一定需要一个返回值，存储过程可以没有参数,不需要返回值 
3). 函数return返回值没有返回参数模式，存储过程通过out参数返回值, 如果需要返回多个参数则建议使用存储过程 
4). 在sql数据操纵语句中只能调用函数而不能调用存储过程

4. Oracle的导入导出有几种方式，有何区别？ 
1). 使用oracle工具 exp/imp 
2). 使用plsql相关工具 
方法1. 导入/导出的是二进制的数据， 2.plsql导入/导出的是sql语句的文本文件 
5. Oracle中有哪几种文件？ 
数据文件（一般后缀为.dbf或者.ora），日志文件(后缀名.log)，控制文件（后缀名为.ctl）

6. 怎样优化Oracle数据库，有几种方式？ 
个人理解，数据库性能最关键的因素在于IO，因为操作内存是快速的，但是读写磁盘是速度很慢的，优化数据库最关键的问题在于减少磁盘的IO，就个人理解应该分为物理的和逻辑的优化， 物理的是指oracle产品本身的一些优化，逻辑优化是指应用程序级别的优化 
物理优化的一些原则： 
1). Oracle的运行环境（网络，硬件等） 
2). 使用合适的优化器 
3). 合理配置oracle实例参数 
4). 建立合适的索引（减少IO） 
5). 将索引数据和表数据分开在不同的表空间上（降低IO冲突） 
6). 建立表分区，将数据分别存储在不同的分区上（以空间换取时间，减少IO） 
   逻辑上优化： 
1). 可以对表进行逻辑分割，如中国移动用户表，可以根据手机尾数分成10个表，这样对性能会有一定的作用 
2). Sql语句使用占位符语句，并且开发时候必须按照规定编写sql语句（如全部大写，全部小写等）oracle解析语句后会放置到共享池中 
如： select * from Emp where name=?  这个语句只会在共享池中有一条，而如果是字符串的话，那就根据不同名字存在不同的语句，所以占位符效率较好 
3). 数据库不仅仅是一个存储数据的地方，同样是一个编程的地方，一些耗时的操作，可以通过存储过程等在用户较少的情况下执行，从而错开系统使用的高峰时间，提高数据库性能 
4). 尽量不使用*号，如select * from Emp，因为要转化为具体的列名是要查数据字典，比较耗时 
5). 选择有效的表名 
对于多表连接查询，可能oracle的优化器并不会优化到这个程度， oracle 中多表查询是根据FROM字句从右到左的数据进行的，那么最好右边的表（也就是基础表）选择数据较少的表，这样排序更快速，如果有link表（多对多中间表），那么将link表放最右边作为基础表，在默认情况下oracle会自动优化，但是如果配置了优化器的情况下，可能不会自动优化，所以平时最好能按照这个方式编写sql 
6). Where字句 规则 
Oracle 中Where字句时从右往左处理的，表之间的连接写在其他条件之前，能过滤掉非常多的数据的条件，放在where的末尾， 另外!=符号比较的列将不使用索引，列经过了计算（如变大写等）不会使用索引（需要建立起函数）， is null、is not null等优化器不会使用索引 
7). 使用Exits Not Exits 替代 In  Not in 
8). 合理使用事务，合理设置事务隔离性 
数据库的数据操作比较消耗数据库资源的，尽量使用批量处理，以降低事务操作次数

7. Oracle中字符串用什么符号链接？ 
Oracle中使用 || 这个符号连接字符串 如 ‘abc’ || ‘d’ 
8. Oracle分区是怎样优化数据库的? 
Oracle的分区可以分为：列表分区、范围分区、散列分区、复合分区。 
1).  增强可用性：如果表的一个分区由于系统故障而不能使用，表的其余好的分区仍可以使用； 
2).  减少关闭时间：如果系统故障只影响表的一部份分区，那么只有这部份分区需要修复，可能比整个大表修复花的时间更少； 
3).  维护轻松：如果需要得建表，独产管理每个公区比管理单个大表要轻松得多； 
4).  均衡I/O：可以把表的不同分区分配到不同的磁盘来平衡I/O改善性能； 
5).  改善性能：对大表的查询、增加、修改等操作可以分解到表的不同分区来并行执行，可使运行速度更快 
6).  分区对用户透明，最终用户感觉不到分区的存在。

9. Oracle是怎样分页的？ 
Oracle中使用rownum来进行分页, 这个是效率最好的分页方法，hibernate也是使用rownum来进行oralce分页的 
select * from 
  ( select rownum r,a from tabName where rownum <= 20 ) 
where r > 10 
10. Oralce怎样存储文件，能够存储哪些文件？ 
Oracle 能存储 clob、nclob、 blob、 bfile 
Clob  可变长度的字符型数据，也就是其他数据库中提到的文本型数据类型 
Nclob 可变字符类型的数据，不过其存储的是Unicode字符集的字符数据 
Blob  可变长度的二进制数据 
Bfile  数据库外面存储的可变二进制数据 
11. Oracle中使用了索引的列，对该列进行where条件查询、分组、排序、使用聚集函数，哪些用到了索引？ 
均会使用索引， 值得注意的是复合索引（如在列A和列B上建立的索引）可能会有不同情况 
12. 数据库怎样实现每隔30分钟备份一次？ 
通过操作系统的定时任务调用脚本导出数据库

13. Oracle中where条件查询和排序的性能比较？ 
Order by使用索引的条件极为严格，只有满足如下情况才可以使用索引， 
1). order by中的列必须包含相同的索引并且索引顺序和排序顺序一致 
2). 不能有null值的列 
所以排序的性能往往并不高，所以建议尽量避免order by

14. 解释冷备份和热备份的不同点以及各自的优点？ 
冷备份发生在数据库已经正常关闭的情况下，将关键性文件拷贝到另外位置的一种说法 
热备份是在数据库运行的情况下，采用归档方式备份数据的方法 
冷备的优缺点： 
1)．是非常快速的备份方法（只需拷贝文件）  
2)．容易归档（简单拷贝即可）  
3)．容易恢复到某个时间点上（只需将文件再拷贝回去）  
4)．能与归档方法相结合，作数据库“最新状态”的恢复。  
5)．低度维护，高度安全。  
冷备份不足：  
1)．单独使用时，只能提供到“某一时间点上”的恢复。  
2)．在实施备份的全过程中，数据库必须要作备份而不能作其它工作。也就是说，在冷备份过程中，数据库必须是关闭状态。  
3)．若磁盘空间有限，只能拷贝到磁带等其它外部存储设备上，速度会很慢。  
4)．不能按表或按用户恢复。  

热备的优缺点 
1)．可在表空间或数据文件级备份，备份时间短。  
2)．备份时数据库仍可使用。  
3)．可达到秒级恢复（恢复到某一时间点上）。  
4)．可对几乎所有数据库实体作恢复。  
5)．恢复是快速的，在大多数情况下在数据库仍工作时恢复。  
热备份的不足是：  
  1)．不能出错，否则后果严重。  
  2)．若热备份不成功，所得结果不可用于时间点的恢复。  
  3)．因难于维护，所以要特别仔细小心，不允许“以失败而告终”。 

15. 解释data block , extent 和 segment的区别？ 
data block 数据块，是oracle最小的逻辑单位，通常oracle从磁盘读写的就是块 
extent 区，是由若干个相邻的block组成 
segment段，是有一组区组成 
tablespace表空间，数据库中数据逻辑存储的地方，一个tablespace可以包含多个数据文件 
16. 比较truncate和delete命令 ？ 
1). Truncate 和delete都可以将数据实体删掉，truncate 的操作并不记录到 rollback日志，所以操作速度较快，但同时这个数据不能恢复 
2). Delete操作不腾出表空间的空间 
3). Truncate 不能对视图等进行删除 
4). Truncate是数据定义语言（DDL），而delete是数据操纵语言(DML) 
17. 解释什么是死锁，如何解决Oracle中的死锁？ 
简言之就是存在加了锁而没有解锁，可能是使用锁没有提交或者回滚事务，如果是表级锁则不能操作表，客户端处于等在状态，如果是行级锁则不能操作锁定行 
解决办法： 
1). 查找出被锁的表 
select b.owner,b.object_name,a.session_id,a.locked_mode 
from v$locked_object a,dba_objects b 
where b.object_id = a.object_id; 
     
select b.username,b.sid,b.serial#,logon_time 
from v$locked_object a,v$session b 
where a.session_id = b.sid order by b.logon_time; 
2). 杀进程中的会话 
alter system kill session "sid,serial#"; 
18. 简述oracle中 dml、ddl、dcl的使用 
Dml 数据操纵语言，如select、update、delete，insert 
Ddl 数据定义语言，如create table 、drop table 等等 
Dcl 数据控制语言， 如 commit、 rollback、grant、 invoke等 
19. 说说oracle中的经常使用到得函数 
Length 长度、 lower 小写、upper 大写， to_date 转化日期， to_char转化字符 
Ltrim 去左边空格、 rtrim去右边空格，substr取字串，add_month增加或者减掉月份、to_number转变为数字 
20. 怎样创建一个存储过程, 游标在存储过程怎么使用, 有什么好处? 
附：存储过程的一般格式，游标使用参考问题 
1 .使用游标可以执行多个不相关的操作.如果希望当产生了结果集后,对结果集中的数据进行多种不相关的数据操作 
2. 使用游标可以提供脚本的可读性 
3. 使用游标可以建立命令字符串,使用游标可以传送表名,或者把变量传送到参数中,以便建立可以执行的命令字符串. 
但是个人认为游标操作效率不太高，并且使用时要特别小心，使用完后要及时关闭 
存储过程优缺点： 
优点： 
1. 存储过程增强了SQL语言的功能和灵活性。存储过程可以用流控制语句编写，有很强的灵活性，可以完成复杂的判断和较复杂的运算。 
2. 可保证数据的安全性和完整性。 
3． 通过存储过程可以使没有权限的用户在控制之下间接地存取数据库，从而保证数据的安全。 
      通过存储过程可以使相关的动作在一起发生，从而可以维护数据库的完整性。 
3. 再运行存储过程前，数据库已对其进行了语法和句法分析，并给出了优化执行方案。这种已经编译好的过程可极大地改善SQL语句的性能。 由于执行SQL语句的大部分工作已经完成，所以存储过程能以极快的速度执行。 
4. 可以降低网络的通信量, 不需要通过网络来传送很多sql语句到数据库服务器了 
5. 使体现企业规则的运算程序放入数据库服务器中，以便集中控制 
       当企业规则发生变化时在服务器中改变存储过程即可，无须修改任何应用程序。企业规则的特点是要经常变化，如果把体现企业规则的运算程序放入应用程序中，则当企业规则发生变化时，就需要修改应用程序工作量非常之大（修改、发行和安装应用程序）。如果把体现企业规则的 运算放入存储过程中，则当企业规则发生变化时，只要修改存储过程就可以了，应用程序无须任何变化。 
缺点： 
1. 可移植性差 
2. 占用服务器端多的资源，对服务器造成很大的压力 
3. 可读性和可维护性不好 

Create  [or replace]  procedure 过程名字（参数 …）as 
vs_ym_sn_end CHAR(6);     --同期终止月份 
CURSOR cur_1 IS   --定义游标(简单的说就是一个可以遍历的结果集) 
SELECT area_code,CMCODE,SUM(rmb_amt)/10000 rmb_amt_sn,SUM(usd_amt)/10000 usd_amt_sn 
FROM BGD_AREA_CM_M_BASE_T 
  WHERE ym >= vs_ym_sn_beg 
  AND ym <= vs_ym_sn_end 
GROUP BY area_code,CMCODE; 
BEGIN 
--用输入参数给变量赋初值，用到了Oralce的SUBSTR TO_CHAR ADD_MONTHS TO_DATE 等很常用的函数。 
vs_ym_beg := SUBSTR(is_ym,1,6); 
vs_ym_end := SUBSTR(is_ym,7,6); 
vs_ym_sn_beg := TO_CHAR(ADD_MONTHS(TO_DATE(vs_ym_beg,"yyyymm"), -12),"yyyymm"); 
vs_ym_sn_end := TO_CHAR(ADD_MONTHS(TO_DATE(vs_ym_end,"yyyymm"), -12),"yyyymm"); 
--先删除表中特定条件的数据。 
DELETE FROM xxxxxxxxxxx_T WHERE ym = is_ym; 
  --然后用内置的DBMS_OUTPUT对象的put_line方法打印出影响的记录行数，其中用到一个系统变量SQL%rowcount 
DBMS_OUTPUT.put_line("del上月记录="||SQL%rowcount||"条"); 

INSERT INTO xxxxxxxxxxx_T(area_code,ym,CMCODE,rmb_amt,usd_amt) 
SELECT area_code,is_ym,CMCODE,SUM(rmb_amt)/10000,SUM(usd_amt)/10000 
FROM BGD_AREA_CM_M_BASE_T 
  WHERE ym >= vs_ym_beg 
  AND ym <= vs_ym_end 
GROUP BY area_code,CMCODE; 

DBMS_OUTPUT.put_line("ins当月记录="||SQL%rowcount||"条"); 
--遍历游标处理后更新到表。遍历游标有几种方法，用for语句是其中比较直观的一种。 
FOR rec IN cur_1 LOOP 
  UPDATE xxxxxxxxxxx_T 
  SET rmb_amt_sn = rec.rmb_amt_sn,usd_amt_sn = rec.usd_amt_sn 
   WHERE area_code = rec.area_code 
   AND CMCODE = rec.CMCODE 
   AND ym = is_ym; 
END LOOP; 
COMMIT; 
--错误处理部分。OTHERS表示除了声明外的任意错误。SQLERRM是系统内置变量保存了当前错误的详细信息。 
EXCEPTION 
   WHEN OTHERS THEN 
      vs_msg := "ERROR IN xxxxxxxxxxx_p("||is_ym||"):"||SUBSTR(SQLERRM,1,500); 
   ROLLBACK; 
   --把当前错误记录进日志表。 
   INSERT INTO LOG_INFO(proc_name,error_info,op_date) 
   VALUES("xxxxxxxxxxx_p",vs_msg,SYSDATE); 
   COMMIT; 
   RETURN; 
END; 
21. 怎样创建一个一个索引,索引使用的原则,有什么优点和缺点 
创建标准索引： 
CREATE  INDEX 索引名 ON 表名 (列名)  TABLESPACE 表空间名; 
创建唯一索引: 
CREATE unique INDEX 索引名 ON 表名 (列名)  TABLESPACE 表空间名; 
创建组合索引: 
CREATE INDEX 索引名 ON 表名 (列名1,列名2)  TABLESPACE 表空间名; 
创建反向键索引: 
CREATE INDEX 索引名 ON 表名 (列名) reverse TABLESPACE 表空间名; 
索引使用原则： 
索引字段建议建立NOT NULL约束 
经常与其他表进行连接的表，在连接字段上应该建立索引； 
经常出现在Where子句中的字段且过滤性很强的，特别是大表的字段，应该建立索引； 
可选择性高的关键字 ，应该建立索引； 
可选择性低的关键字，但数据的值分布差异很大时，选择性数据比较少时仍然可以利用索引提高效率 
复合索引的建立需要进行仔细分析；尽量考虑用单字段索引代替： 
A、正确选择复合索引中的第一个字段，一般是选择性较好的且在where子句中常用的字段上； 
B、复合索引的几个字段经常同时以AND方式出现在Where子句中可以建立复合索引；否则单字段索引； 
C、如果复合索引中包含的字段经常单独出现在Where子句中，则分解为多个单字段索引； 
D、如果复合索引所包含的字段超过3个，那么仔细考虑其必要性，考虑减少复合的字段； 
E、如果既有单字段索引，又有这几个字段上的复合索引，一般可以删除复合索引； 
频繁DML的表，不要建立太多的索引； 
不要将那些频繁修改的列作为索引列； 
索引的优缺点： 
有点： 
1. 创建唯一性索引，保证数据库表中每一行数据的唯一性 
2. 大大加快数据的检索速度，这也是创建索引的最主要的原因 
3. 加速表和表之间的连接，特别是在实现数据的参考完整性方面特别有意义。 
4. 在使用分组和排序子句进行数据检索时，同样可以显著减少查询中分组和排序的时间。 
缺点： 
1. 索引创建在表上，不能创建在视图上 
2. 创建索引和维护索引要耗费时间，这种时间随着数据量的增加而增加 
3. 索引需要占物理空间，除了数据表占数据空间之外，每一个索引还要占一定的物理空间，如果要建立聚簇索引，那么需要的空间就会更大 
4. 当对表中的数据进行增加、删除和修改的时候，索引也要动态的维护，降低了数据的维护速度 

22. 怎样创建一个视图,视图的好处, 视图可以控制权限吗? 
create view 视图名 as select 列名 [别名]  …  from 表 [unio [all] select … ] ] 
好处： 
1. 可以简单的将视图理解为sql查询语句，视图最大的好处是不占系统空间 
2. 一些安全性很高的系统，不会公布系统的表结构，可能会使用视图将一些敏感信息过虑或者重命名后公布结构 
3. 简化查询 
可以控制权限的，在使用的时候需要将视图的使用权限grant给用户 
23. 怎样创建一个触发器, 触发器的定义, 触发器的游标怎样定义 
CREATE [OR REPLACE] TIGGER触发器名 触发时间 触发事件 
　ON表名 
　[FOR EACH ROW] 
　BEGIN 
　　pl/sql语句 
    CURSOR  游标名 is  SELECT * FROM 表名 （定义游标） 
　　END 
　其中： 
　触发器名：触发器对象的名称。 
　由于触发器是数据库自动执行的，因此该名称只是一个名称，没有实质的用途。 
触发时间：指明触发器何时执行，该值可取： 
before---表示在数据库动作之前触发器执行; 
after---表示在数据库动作之后出发器执行。 
触发事件：指明哪些数据库动作会触发此触发器：                       
　　 insert：数据库插入会触发此触发器;  

24. oracle创建表的几种方式;应该注意些什么 
不知道这个题目是不是记错了，感觉很怪 
1. 使用图形工具创建表 
2. 使用数据ddl语句创建表 
3. 可以在plsql代码中动态创建表 
应该注意： 是否有创建表的权限， 使用什么表空间等 
25. 怎样将一个旧数据库数据移到一个新的数据库 
1. Imp/exp将数据库中的数据导入到新的库中 
2. 如果是存储迁移直接将存储设备挂到新机器上 
26. 主键有几种; 
字符型，整数型、复合型 
27. oracle的锁又几种,定义分别是什么; 
1.  行共享锁 (ROW SHARE) 
2.  行排他锁(ROW EXCLUSIVE) 
3 . 共享锁(SHARE) 
4.  共享行排他锁(SHARE ROW EXCLUSIVE) 
5.  排他锁(EXCLUSIVE) 
使用方法： 
SELECT * FROM order_master WHERE vencode="V002" 
FOR UPDATE WAIT 5; 
LOCK TABLE order_master IN SHARE MODE; 
LOCK TABLE itemfile IN EXCLUSIVE MODE NOWAIT; 
ORACLE锁具体分为以下几类： 
1.按用户与系统划分，可以分为自动锁与显示锁 
自动锁：当进行一项数据库操作时，缺省情况下，系统自动为此数据库操作获得所有有必要的锁。 
显示锁：某些情况下，需要用户显示的锁定数据库操作要用到的数据，才能使数据库操作执行得更好，显示锁是用户为数据库对象设定的。 
2 . 按锁级别划分，可分为共享锁与排它锁 
共享锁：共享锁使一个事务对特定数据库资源进行共享访问——另一事务也可对此资源进行访问或获得相同共享锁。共享锁为事务提供高并发性，但如拙劣的事务设计+共享锁容易造成死锁或数据更新丢失。 
排它锁：事务设置排它锁后，该事务单独获得此资源，另一事务不能在此事务提交之前获得相同对象的共享锁或排它锁。 
3.按操作划分，可分为DML锁、DDL锁 
DML锁又可以分为，行锁、表锁、死锁 
行锁：当事务执行数据库插入、更新、删除操作时，该事务自动获得操作表中操作行的排它锁。 
表级锁：当事务获得行锁后，此事务也将自动获得该行的表锁(共享锁),以防止其它事务进行DDL语句影响记录行的更新。事务也可以在进行过程中获得共享锁或排它锁，只有当事务显示使用LOCK TABLE语句显示的定义一个排它锁时，事务才会获得表上的排它锁,也可使用LOCK TABLE显示的定义一个表级的共享锁(LOCK TABLE具体用法请参考相关文档)。 
死锁：当两个事务需要一组有冲突的锁，而不能将事务继续下去的话，就出现死锁。 
如事务1在表A行记录#3中有一排它锁，并等待事务2在表A中记录#4中排它锁的释放，而事务2在表A记录行#4中有一排它锁，并等待事务; 1在表A中记录#3中排它锁的释放，事务1与事务2彼此等待，因此就造成了死锁。死锁一般是因拙劣的事务设计而产生。死锁只能使用SQL下:alter system kill session "sid,serial#"；或者使用相关操作系统kill进程的命令，如UNIX下kill -9 sid,或者使用其它工具杀掉死锁进程。 
DDL锁又可以分为：排它DDL锁、共享DDL锁、分析锁 
排它DDL锁：创建、修改、删除一个数据库对象的DDL语句获得操作对象的 排它锁。如使用alter table语句时，为了维护数据的完成性、一致性、合法性，该事务获得一排它DDL锁。 
共享DDL锁：需在数据库对象之间建立相互依赖关系的DDL语句通常需共享获得DDL锁。 
如创建一个包，该包中的过程与函数引用了不同的数据库表，当编译此包时，该事务就获得了引用表的共享DDL锁。 
分析锁：ORACLE使用共享池存储分析与优化过的SQL语句及PL/SQL程序，使运行相同语句的应用速度更快。一个在共享池中缓存的对象获得它所引用数据库对象的分析锁。分析锁是一种独特的DDL锁类型，ORACLE使用它追踪共享池对象及它所引用数据库对象之间的依赖关系。当一个事务修改或删除了共享池持有分析锁的数据库对象时，ORACLE使共享池中的对象作废，下次在引用这条SQL/PLSQL语句时，ORACLE重新分析编译此语句。 
4.内部闩锁 
内部闩锁：这是ORACLE中的一种特殊锁，用于顺序访问内部系统结构。当事务需向缓冲区写入信息时，为了使用此块内存区域，ORACLE首先必须取得这块内存区域的闩锁，才能向此块内存写入信息。 

28. 在java种怎样调用oracle存储过程; 
在java中使用 CallableStatement调用存储过程 
创建需要的测试表:create table Test(tid varchar2(10),tname varchar2(10)); 
  第一种情况：无返回值. 
      create or replace procedure test_a(param1 in varchar2,param2 in varchar2) as 
       begin 
            insert into test value(param1,param2); 
     end; 
Java调用代码: 
package com.test; 
import java.sql.*; 
import java.io.*; 
import java.sql.*; 
public class TestProcA 
{ 
   public TestProcA(){ 
   } 
   public static void main(String []args) 
   { 
        ResultSet rs = null; 
        Connection conn = null; 
        CallableStatement proc = null; 
        try{ 
       Class.forName("oracle.jdbc.driver.OracleDriver"); 
conn =  DriverManager.getConnection("jdbc:oracle:thin:@127.0.0.1:1521:test", "test", "test"); 
          proc = conn.prepareCall("{ call test_a(?,?) }"); 
          proc.setString(1, "1001"); 
          proc.setString(2, "TestA"); 
          proc.execute(); 
        }catch(Exception e){ 
     e.printStackTrace(); 
}finally{ 
           try{ 
       if(null!=rs){ 
                 rs.close(); 

          if(null!=proc){ 
                    proc.close(); 
          } 

          if(null!=conn){ 
                    conn.close(); 
          } 
       }  
           }catch(Exception ex){ 
           } 
        } 
   } 
} 

第二种情况：有返回值的存储过程(返回值非列表). 
存储过程为: 
create or replace procedure test_b(param1 in varchar2,param2 out varchar2) 
as 
begin 
    select tname into param2 from test where tid=param1; 
end; 

Java调用代码： 
package com.test; 
import java.sql.*; 
import java.io.*; 
import java.sql.*; 

public class TestProcB 
{ 
   public TestProcB(){ 
   } 
   public static void main(String []args) 
   { 
        Connection conn = null; 
        CallableStatement proc = null; 
       
        try{ 
          Class.forName("oracle.jdbc.driver.OracleDriver"); 
          conn =  DriverManager.getConnection("jdbc:oracle:thin:@127.0.0.1:1521:test", "test", "test"); 
          proc = conn.prepareCall("{ call test_b(?,?) }"); 
          proc.setString(1, "1001"); 
          proc.registerOutParameter(2, Types.VARCHAR); 
          proc.execute(); 
          System.out.println("Output is:"+proc.getString(2)); 
        }catch(Exception e){ 
     e.printStackTrace(); 
}finally{ 
           try{ 
          if(null!=proc){ 
                    proc.close(); 
          } 

          if(null!=conn){ 
                    conn.close(); 
          } 

           }catch(Exception ex){ 
           } 
        } 
   } 
} 

第三种情况：返回列表. 

由于oracle存储过程没有返回值，它的所有返回值都是通过out参数来替代的，列表同样也不例外，但由于是集合，所以不能用一般的参数，必须要用pagkage了.要分两部分来写： 
create or replace package tpackage as 
type t_cursor is ref cursor; 
procedure test_c(c_ref out t_cursor); 
end ; 

create or replace package body tpackage as 
procedure test_c(c_ref out t_cursor) is 
   begin 
      open c_ref for select * from test; 
  end test_c; 
end tpackage; 

Java调用代码： 
package com.test; 
import java.sql.*; 
import java.io.*; 
import java.sql.*; 

public class TestProcB 
{ 
   public TestProcB(){ 
   } 
   
   public static void main(String []args) 
   { 
        Connection conn = null; 
        CallableStatement proc = null; 
        ResultSet rs =  null; 
        try{ 
          Class.forName("oracle.jdbc.driver.OracleDriver"); 
          conn =  DriverManager.getConnection("jdbc:oracle:thin:@127.0.0.1:1521:test", "test", "test"); 
          proc = conn.prepareCall("{? = call tpackage.test_b(?) }"); 
           
          proc.registerOutParameter(1, OracleTypes.CURSOR); 
          proc.execute(); 
          while(rs.next()){ 
              System.out.println(rs.getObject(1) + "\t" + rs.getObject(2)); 
          } 
        }catch(Exception e){ 
     e.printStackTrace(); 
}finally{ 
           try{ 
          if(null!=rs){ 
              rs.close(); 
             if(null!=proc){ 
                    proc.close(); 
             } 

             if(null!=conn){ 
                    conn.close(); 
             } 
          } 
          }catch(Exception ex){ 
           } 
        } 
   } 
} 

29. rowid, rownum的定义 
1. rowid和rownum都是虚列 
2. rowid是物理地址，用于定位oracle中具体数据的物理存储位置 
3. rownum则是sql的输出结果排序，从下面的例子可以看出其中的区别。 
30. oracle中存储过程，游标和函数的区别 
游标类似指针，游标可以执行多个不相关的操作.如果希望当产生了结果集后,对结果集中的数据进行多 种不相关的数据操作 
函数可以理解函数是存储过程的一种； 函数可以没有参数,但是一定需要一个返回值，存储过程可以没有参数,不需要返回值；两者都可以通过out参数返回值, 如果需要返回多个参数则建议使用存储过程；在sql数据操纵语句中只能调用函数而不能调用存储过程 
31. 使用oracle 伪列删除表中重复记录： 
Delete  table t  where t.rowid!=(select  max(t1.rowid)  from  table1 t1 where  t1.name=t.name)
```