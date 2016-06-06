#!/bin/bash

cnt=0

if [ ! -d sbin/simpleweb ]; then echo no simpleweb; exit 1; fi
echo $$ >> logpid

while [ true ]; do

  echo 
  echo '=================================';
  cnt=$(($cnt + 1))
  echo '    ' cnt $cnt timestamp $(date +%s)
  echo -n '    ' ; date ; echo

  result=unknown
  savefil=$(printf "save%03d_%s" $cnt $result)
  echo savefil $savefil

  killall mosquitto ; sleep 3
  if [ -f log-runon-mosquitto ]; then rm log-runon-mosquitto; fi

  if [ -f newbuild ]; then mv newbuild sbin/mosquitto; echo newbuild; fi

  sh run_on_openshift.sh start 
  sleep 300
  ps -e | grep mosq
  if [ $? -eq 0 ]; then result=succ; else result=fail; fi
  echo result $result cnt $cnt

  killall mosquitto ; sleep 3
  savefil=$(printf "save%03d_%s" $cnt $result)
  if [ ! -d savedlogs ]; then mkdir savedlogs; fi
  mv log-runon-mosquitto savedlogs/$savefil

  echo
  echo '    ' cnt $cnt timestamp $(date +%s) done
  echo -n '    ' ; date
  echo '=================================';

done


