#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

echo "  "
echo "  DIR $DIR"
echo "  " pwd
echo -n "  "
pwd

sleep 1

dir2=$OPENSHIFT_REPO_DIR/uploaddata
dir1=$OPENSHIFT_DATA_DIR/uploaddata

if [ ! -d $dir1 ] ; then
    echo Error no dir1 $dir1
    exit 1
fi
if [ ! -d $dir2 ] ; then
    echo Creating dir2 $dir2
    mkdir $dir2
fi
echo "  "
echo "rsync -rtlv $dir1/ $dir2/"
      rsync -rtlv $dir1/ $dir2/

dir2=$OPENSHIFT_REPO_DIR/uploadlist
dir1=$OPENSHIFT_DATA_DIR/uploadlist

if [ ! -d $dir1 ] ; then
    echo Error no dir1 $dir1
    exit 1
fi
if [ ! -d $dir2 ] ; then
    echo Creating dir2 $dir2
    mkdir $dir2
fi
echo "  "
echo "rsync -rtlv $dir1/ $dir2/"
      rsync -rtlv $dir1/ $dir2/


