#!/bin/bash

#30 day 24 hr 60 min 60 sec / sleep 10
loopmax=$(( 30 * 24 * 60 * 60 / 10))

loopcnt=0

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
echo "DIR $DIR"  > log9.txt
echo pwd >> log9.txt
pwd >> log9.txt
datestr=`date +"%2m%2d %2H%2M%2S"`
echo $datestr >> log9.txt
mypid=$$
echo "mypid $mypid" >> log9.txt
ls -ld /proc/$mypid/exe >> log9.txt
cp log9.txt ${OPENSHIFT_DATA_DIR}

while [ $loopcnt -lt $loopmax ] ; do
  datestr=`date +"%2m%2d %2H%2M%2S"`
  looprsd=$(( $loopcnt % 6 ))
  if [ $looprsd -eq 0 ] ; then 
      echo $datestr > log1.txt
  elif [ $looprsd -eq 1 ] ; then 
      echo $datestr > log2.txt
  elif [ $looprsd -eq 2 ] ; then 
      echo $datestr > log3.txt
  elif [ $looprsd -eq 3 ] ; then 
      echo $datestr > log4.txt
  elif [ $looprsd -eq 4 ] ; then 
      echo $datestr > log5.txt
  elif [ $looprsd -eq 5 ] ; then 
      echo $datestr > log6.txt
  else
      echo $datestr > log7.txt
  fi
  sleep 10
  echo loopcnt $loopcnt > log8.txt
  echo $datestr >> log8.txt
  cp log8.txt ${OPENSHIFT_DATA_DIR}
  let 'loopcnt = loopcnt + 1'
done

echo done >> log8.txt
cp log8.txt ${OPENSHIFT_DATA_DIR}


