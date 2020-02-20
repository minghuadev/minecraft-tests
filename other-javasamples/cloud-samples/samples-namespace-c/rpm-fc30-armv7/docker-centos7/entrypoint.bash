#!/bin/bash
# entrypoint.bash

logf=${HOME}/log-entrypoint-loop

cnt=0
(echo pwd; pwd ) > $logf
(echo date; date ) >> $logf
while true ; do
	cnt=$(( ${cnt} + 1 ))
	(echo ; echo date; date; echo cnt $cnt ) >> $logf
	sleep 10
done

