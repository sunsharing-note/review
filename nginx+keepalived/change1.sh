
#!/bin/bash
 
change_name(){
DIR=/oldboy
FILE=`ls /oldboy`
GIRL=_oldgirl.HTML
 
for i in $FILE
do
   c=`echo $i | cut -c 1-10`
   mv $DIR/$c* $DIR/$c$GIRL
done
}
 
