
#!/bin/bash
 
tmp_fifofile=/tmp/$$.fifo
mkfifo $tmp_fifofile
exec 6<> $tmp_fifofile
rm -rf $tmp_fifofile
 
thread=254
for ((i=0;i<$thread;i++))
do
    echo >&6
done
 
for ((i=2;i<255;i++))
do
read -u6
    {
        ip=172.16.27.
        ping $ip$i -c 1 >/dev/null && echo $ip$i:live || echo $ip$i:dead >>123
               echo >&6
    }&
done
wait
exec 6>&-
 
exit 0
