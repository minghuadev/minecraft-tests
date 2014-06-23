#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

echo "  "
echo "  DIR $DIR"
echo "  " pwd
echo -n "  "
pwd

sleep 1
echo "  "
echo "  Starting nohup bash test_loop.sh ..."
echo "  "

nohup bash test_loop.sh > loga.txt 2>&1 &

sleep 1
echo "  "
echo "  Starting nohup bash test_loop.sh ... done."
echo "  "

echo "  log1..6 ---- normal log"
echo "  log7 ------- else-case log"
echo "  log8 --- --- current loopcnt log and done line log"
echo "  log9 ------- startup dir log"
echo "  loga ------- nohup log"
echo "  "


