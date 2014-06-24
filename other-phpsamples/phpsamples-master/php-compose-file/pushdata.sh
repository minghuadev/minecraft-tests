#!/bin/sh
#pushdata.sh

cnt=0
ocnt=0

site=mysite.hosting.org

if [ ! -d /tmp/datatmp ]; then mkdir /tmp/datatmp; fi

while true
do

  let 'cnt = cnt + 1'
  minstr=`date +"%M"`
  secstr=`date +"%S"`
  if [ $minstr -eq 0 ]; then ocnt=0; fi
  let 'ocnt = ocnt + 1'

  n=`cat /tmp/datatmp/data | wc -l`

  ocnt=$((ocnt%30))
  if [ $ocnt -eq 1 ] ; then
      cat req2lf | nc -c $site 80
      if [ $? -ne 0 ]; then echo error req2lf; fi
      cat req1dt | nc -c $site 80
      if [ $? -ne 0 ]; then echo error req1dt; fi
  fi
  printf "%03d" $n > /tmp/datatmp/datawcl
  (cat req3h1 ; echo -n `cat /tmp/datatmp/datawcl` ; cat req3h3 ) | nc -c $site 80
  if [ $? -ne 0 ]; then echo error req3h; fi

  if [ $secstr -gt 45 ]; then
      sleep 40
  else
      sleep 60
  fi

done

