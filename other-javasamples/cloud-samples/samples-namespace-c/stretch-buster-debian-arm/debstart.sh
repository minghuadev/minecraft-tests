#!/bin/sh
# debstart.sh

# config
EXT_CONTAINER_PATH="/root/debian_layer"
EXT_CONTAINER_PARENT="root-debian-parent"

# scripts
olddir=$(pwd)
thisprog=$0

cd ${EXT_CONTAINER_PATH}
while true; do # scope 
    if [ -z "$1" ]; then break; fi
    cmd=$1
    if [ "$cmd" == "sh_bash" ]; then
        echo Running pivot ...
        pivot_root . ${EXT_CONTAINER_PARENT}

        echo Running bash ...
        bash

        echo Running exit ...
        exit 0
    elif [ "$cmd" == "sh_systemd" ]; then
        echo Running pivot ...
        pivot_root . ${EXT_CONTAINER_PARENT}
        #/lib/ld-2.30.so /usr/lib/systemd/systemd --system --unit=basic.target
        /lib/ld-2.30.so /usr/lib/systemd/systemd --help

        echo Running exit ...
        exit 0
    fi
    break # scope
done # while true scope 

mount -o bind /proc proc
mount -o bind /dev dev
mount -o bind /dev/pts dev/pts
mount -o bind /sys sys
mount -t tmpfs tmpfs run

echo Running unshare ...
if [ ! -z "$1" -a "$1" == "bash" ]; then 
    unshare -p -m --propagation slave  sh -c "cd $olddir && $thisprog sh_bash"
else
    unshare  -m --propagation slave  root/debian_init
fi

echo Running umount ...
umount run
umount sys
umount dev/pts
umount dev
umount proc

echo Running cd '$'olddir ...
cd $olddir


