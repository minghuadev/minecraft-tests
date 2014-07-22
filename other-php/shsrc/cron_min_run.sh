#!/bin/bash
#cron_min_run.sh derived from test_loop.sh

export TZ='America/Los_Angeles'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

echo "DIR $DIR"  >> log9.txt
echo pwd >> log9.txt
pwd >> log9.txt
datestr=`date +"%2m%2d %2H%2M%2S"`
echo $datestr >> log9.txt
mypid=$$
echo "mypid $mypid" >> log9.txt
ls -ld /proc/$mypid/exe >> log9.txt
cp log9.txt ${OPENSHIFT_DATA_DIR}


  datestr=`date +"%2m%2d %2H%2M%2S"`

  datehr=$(date +"%2H")
  datemi=$(date +"%2M")
  datese=$(date +"%2S")

  if [ $datehr -ge 18 ] ; then 
      if [ ! -f log8.txt ]; then
          echo  " "  >> log8.txt
          echo  $datestr >> log8.txt
          echo  " "  >> log8.txt
          cp log8.txt ${OPENSHIFT_DATA_DIR}

          echo  " "  >> log7.txt
          echo  $datestr >> log7.txt
          echo  " "  >> log7.txt
          bash ci_auto_daily.sh
          cd $DIR
          echo  " "  >> log7.txt
          cp log7.txt ${OPENSHIFT_DATA_DIR}
      fi
  else
      if [ -f log8.txt ]; then
          rm log8.txt
      fi
  fi

datestr=`date +"%2m%2d %2H%2M%2S"`
echo $datestr >> log9.txt
echo " " >> log9.txt
cp log9.txt ${OPENSHIFT_DATA_DIR}


exit 0

#
# in .openshift/cron/minutely/cron_min.sh: 
#
#    date > ${OPENSHIFT_DATA_DIR}/logb.txt
#    ${OPENSHIFT_REPO_DIR}/shsrc/cron_min_run.sh >> ${OPENSHIFT_DATA_DIR}/logb.txt 2>&1
#

