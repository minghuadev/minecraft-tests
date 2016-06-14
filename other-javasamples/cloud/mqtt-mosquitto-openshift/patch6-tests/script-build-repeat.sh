#!/bin/bash

cnt=0

if [ ! -d ../mosweb/sbin/simpleweb ]; then echo no simpleweb; exit 1; fi

echo $$ >> logpid

while [ true ]; do

  echo 
  echo '=================================';
  cnt=$(($cnt + 1))
  echo '    ' cnt $cnt timestamp $(date +%s)
  echo -n '    ' ; date ; echo

  make clean
  make
  cp src/mosquitto ../mosweb/newbuild
  echo
  echo 'ls -l ../mosweb/newbuild'
  ls -l ../mosweb/newbuild

  sleep 1700

  echo
  echo '    ' cnt $cnt timestamp $(date +%s) done
  echo -n '    ' ; date
  echo '=================================';

  if [ -f ../mosweb/newerror ]; then 
      echo ; echo found ../mosweb/newerror .. stop building 
      break
  fi

done


