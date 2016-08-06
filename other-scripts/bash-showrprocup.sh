#!/bin/bash
# bash-showrprocup.sh  -- show remote proc uptime

rhost=$1
rproc=$2

echo '      ' rhost $rhost '      ' rproc $rproc


rline=`ssh $rhost 'ps | grep '${rproc}' | grep -v grep'`
rpid=`echo $rline | cut -d ' ' -f1`

echo '  ' rline $rline
echo '   ' rpid $rpid


rline=`ssh $rhost cat /proc/uptime`
ruptm=`echo $rline | cut -d '.' -f1`

echo '  ' rline $rline
echo '  ' ruptm $ruptm


rline=`ssh $rhost cat /proc/$rpid/stat`
rpstm=`echo $rline | cut -d ' ' -f22`

echo '  ' rline $rline
echo '  ' rpstm $rpstm


uptm=$(($ruptm - $rpstm/100))
echo '   ' uptm $uptm

uphr=$(($uptm/3600))
echo '   ' uphr $uphr

upmin=$(( ($uptm%3600)/60 ))
echo '  ' upmin $upmin

upsec=$(( $uptm%60 ))
echo '  ' upsec $upsec


