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
echo "  log1..6 ---- normal log"
echo "  "

echo -n "  log1 "; cat log1.txt
echo -n "  log2 "; cat log2.txt
echo -n "  log3 "; cat log3.txt
echo -n "  log4 "; cat log4.txt
echo -n "  log5 "; cat log5.txt
echo -n "  log6 "; cat log6.txt

echo "  "

echo "  "
echo "  log7 ------- else-case log"
echo -n "    "; cat log7.txt
echo "  "

echo "  "
echo "  log8 --- --- current loopcnt log and done line log"
echo -n "    "; cat log8.txt
echo "  "

echo "  "
echo "  log9 ------- startup dir log"
echo -n "    "; cat log9.txt
echo "  "

echo "  "
echo "  loga ------- nohup log"
echo -n "    "; cat loga.txt
echo "  "

