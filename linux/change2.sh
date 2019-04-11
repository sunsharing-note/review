
#!/bin/bash
 
change_name(){
DIR=/oldboy
FILE=`ls /oldboy`
GIRL=_oldgirl.HTML
 
for i in $FILE
do
   c=`echo $i | awk -F '_' '{print $1}'`
   mv $DIR/$c* $DIR/$c$GIRL
done
}
 
change_name
