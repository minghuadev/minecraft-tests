#!/bin/bash -x
# run_on_openshift.sh
#    this file is placed in mosweb folder

wkdir=mosweb
uarg="$1"
  # user arguments must be one of <empty>, "start", "stop", "status"

run_on_openshift=yes
OPENSHIFT_EXT_PORT=8000
    # 8000 is the openshift-online rhel 6.7 default websocket external port
if [ "x$OPENSHIFT_LOG_DIR" == "x" ]; then 
  run_on_openshift=no
  # if running locally mimic the openshift env below
  OPENSHIFT_LOG_DIR=$(pwd)
  OPENSHIFT_REPO_DIR=$(pwd)/..
  OPENSHIFT_GEAR_DNS='127.0.0.1'
  OPENSHIFT_DIY_IP='127.0.0.1'
  OPENSHIFT_DIY_PORT=9008
  OPENSHIFT_EXT_PORT=9008
  echo 
  echo Local run ... "OPENSHIFT_LOG_DIR " $OPENSHIFT_LOG_DIR  ...
  echo Local run ... "OPENSHIFT_REPO_DIR" $OPENSHIFT_REPO_DIR ...
  echo Local run ... "OPENSHIFT_GEAR_DNS" $OPENSHIFT_GEAR_DNS ...
  echo Local run ... "OPENSHIFT_DIY_IP  " $OPENSHIFT_DIY_IP   ...
  echo Local run ... "OPENSHIFT_DIY_PORT" $OPENSHIFT_DIY_PORT  ...
  echo Local run ... "OPENSHIFT_EXT_PORT" $OPENSHIFT_EXT_PORT  ...
  echo 
fi

logfil=$OPENSHIFT_LOG_DIR/log-runon
if [ ! "x_$run_on_openshift" == "x_yes" ]; then
  echo
  echo Log file : $logfil
  echo
fi
  echo 

    function chkfolder() {
        fchk=$1
        if [ "x$fchk" == "x" ]; then
            echo Error : No folder to check. >> $logfil ; exit 1
        fi
        if [ ! -d $fchk ]; then 
            echo Error : No folder $fchk. >> $logfil ; exit 1
        fi
    }
    function chkfile() {
        fchk=$1
        if [ "x$fchk" == "x" ]; then
            echo Error : No file to check. >> $logfil ; exit 1
        fi
        if [ ! -f $fchk ]; then 
            echo Error : No file $fchk. >> $logfil ; exit 1
        fi
    }

echo  >> $logfil ;  date  >> $logfil ; echo -n cmd ' '  >> $logfil ; 
echo $0 >> $logfil

chkfolder $OPENSHIFT_REPO_DIR 
cd $OPENSHIFT_REPO_DIR ; echo -n pwd ' ' >> $logfil
pwd   >> $logfil

chkfolder "$wkdir"
cd $wkdir ; echo -n pwd ' ' >> $logfil
pwd   >> $logfil

  chkfolder sbin
  chkfolder sbin/simpleweb
  chkfile   sbin/simpleweb/config.js

upid=`ps -ef | grep mosquitto | grep -v grep | awk '{ print $2 }'`

if [ "x_$uarg" == "x_stop" ]; then
    # user command "stop"
    echo User argument action stop. upid $upid . >> $logfil
    if [ "x_$run_on_openshift" == "x_yes" ]; then
        source $OPENSHIFT_CARTRIDGE_SDK_BASH
    fi

    # The logic to stop your application should be put in this script.
    if [ -z "$upid" ] ; then
        if [ ! "x_$run_on_openshift" == "x_yes" ]; then
            client_result "Application is already stopped"
        else
            echo "Application is already stopped" >> $logfil
        fi
    else
        echo "Application is being stopped : upid $upid" >> $logfil
        kill $upid > /dev/null 2>&1
    fi
    exit 0
fi

if [ "x_$uarg" == "x_" ]; then
    # user command empty
    echo No user argument. Configure only. >> $logfil
elif [ "x_$uarg" == "x_start" -o "x_$uarg" == "x_status" ]; then
    # user command "start" or "status"
    if [ -z "$upid" ]; then
        echo "User pid: \<empty\>" >> $logfil
    else
        echo "User pid: $upid" >> $logfil
    fi
    if [ "x_$uarg" == "x_start" ]; then
        if [ ! -z "$upid" ]; then
            echo Error : User argument action start. upid $upid . >> $logfil
            exit 1
        fi
    elif [ "x_$uarg" == "x_status" ]; then
        echo User argument action status. upid $upid . >> $logfil
        exit 0
    else
        echo Error : User argument action not start or status. >> $logfil
        exit 1
    fi
else
    # user command unknown
    echo User argument action unknown $uarg. >> $logfil
    exit 1
fi

# user command: empty, or "start"
if [ ! -f sbin/simpleweb/config-orig.js ]; then 
  echo 'Backup: cp -a sbin/simpleweb/config.js sbin/simpleweb/config-orig.js' >> $logfil
  cp -a sbin/simpleweb/config.js sbin/simpleweb/config-orig.js
fi

cp -a sbin/simpleweb/config-orig.js sbin/simpleweb/config.js
sed -i -e s/\^host\ =\ .*/host\ =\ \\\'$OPENSHIFT_GEAR_DNS\\\'\;/ sbin/simpleweb/config.js
sed -i -e s/\^port\ =\ .*/port\ =\ $OPENSHIFT_EXT_PORT\;/ sbin/simpleweb/config.js

if [ ! -f sbin/mosquitto-orig.conf ]; then 
  if [ -f sbin/mosquitto.conf ]; then 
    echo 'Backup: mv sbin/mosquitto.conf sbin/mosquitto-orig.conf' >> $logfil
    mv sbin/mosquitto.conf sbin/mosquitto-orig.conf
  fi
fi
echo listener $OPENSHIFT_DIY_PORT $OPENSHIFT_DIY_IP > sbin/mosquitto.conf
echo protocol websockets  >> sbin/mosquitto.conf
echo http_dir simpleweb   >> sbin/mosquitto.conf
echo connection_messages true >> sbin/mosquitto.conf

cd sbin ; echo -n pwd ' ' >> $logfil
pwd   >> $logfil
if [ "x_$uarg" == "x_start" ]; then
    if [ ! -z "$upid" ]; then
        echo Error : User argument action start. upid $upid . >> $logfil
        exit 1
    fi
  export LD_LIBRARY_PATH=.
  if [ "x_$run_on_openshift" == "x_yes" ]; then
    nohup ./mosquitto -c mosquitto.conf  |& /usr/bin/logshifter -tag diy &
  else
    nohup ./mosquitto -c mosquitto.conf -v > ${logfil}-mosquitto & 
  fi
fi

upid=`ps -ef | grep mosquitto | grep -v grep | awk '{ print $2 }'`
    if [ -z "$upid" ]; then
        echo "User pid: \<empty\>" >> $logfil
    else
        echo "User pid: $upid" >> $logfil
    fi


