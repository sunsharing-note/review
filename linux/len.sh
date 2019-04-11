#! /bin/bash

a="I am oldboy teacher welcome to oldboy training class."
for i in $a
do
  num=`echo $i |wc -L`
  if [ $num -le 6 ];then
     echo $i
  fi
done

echo "##############2############"

for i in $a
do
 if [ ${#i} -le 6 ];then
    echo $i
 fi
done