#!/bin/bash 

host=10.10.10.100


function runone () {
  min=$1
  sec=$(($min * 60))

  mnstr=`date +"%m"`
  dystr=`date +"%d"`
  fn=data${mnstr}${dystr}.txt

  echo
  echo ${fn}
  wget $host/${fn}
  tail -4 ${fn} > data
  rm ${fn}
#  git add data
#  git commit -m 'new data'
#  git push origin master

  echo
  echo sleep $sec mn $mnstr dy $dystr
  sleep $sec
}

while true; do
  hrstr=`date +"%H"`
  if [ $hrstr -ge 7 -a $hrstr -le 12 ]; then 
    runone 5
    runone 55
  elif [ $hrstr -ge 13 -a $hrstr -lt 15 ]; then 
    runone 60
  elif [ $hrstr -ge 15 -a $hrstr -le 18 ]; then 
    runone 15
  elif [ $hrstr -ge 20 -a $hrstr -le 22 ]; then 
    runone 15
  fi
  sleep 60
done

