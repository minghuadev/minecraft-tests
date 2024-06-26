#!/bin/bash

#30 day 24 hr 60 min 60 sec / sleep 10
loopmax=$(( 30 * 24 * 60 * 60 / 10))

loopcnt=0

export TZ='America/Los_Angeles'

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
rm log8.txt
rm log7.txt

while [ $loopcnt -lt $loopmax ] ; do
  datestr=`date +"%2m%2d %2H%2M%2S"`

  datehr=$(date +"%2H")
  datemi=$(date +"%2M")
  datese=$(date +"%2S")

  if [ $datehr -eq 21 ] ; then 
      if [ $datemi -eq 0 ]; then
          echo  " "  >> log7.txt
          echo  $datestr >> log7.txt
          echo  " "  >> log7.txt
          bash ci_auto_daily.sh
          cd $DIR
          echo  " "  >> log7.txt
          cp log7.txt ${OPENSHIFT_DATA_DIR}
      fi
  fi

  if [ $datese -ge 50 ]; then
      sleep 40
  else
      sleep 60
  fi

  echo -n loopcnt $loopcnt " " >> log8.txt
  echo $datestr >> log8.txt
  cp log8.txt ${OPENSHIFT_DATA_DIR}
  let 'loopcnt = loopcnt + 1'
done

echo done >> log8.txt
cp log8.txt ${OPENSHIFT_DATA_DIR}


