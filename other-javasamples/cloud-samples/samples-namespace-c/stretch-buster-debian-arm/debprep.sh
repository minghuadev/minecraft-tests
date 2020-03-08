#!/bin/bash
# container_inner_prepare.sh -- bash script running inside the container

umount /proc/
mount -t proc proc /proc/

umount /sys/fs/cgroup
mount -t tmpfs tmpfs /sys/fs/cgroup/
mkdir /sys/fs/cgroup/systemd
mount -t tmpfs tmpfs /sys/fs/cgroup/systemd
mkdir /sys/fs/cgroup/systemd/lxc

mkdir /container-cgroup
umount /container-cgroup
mount -t cgroup cgroup -o none,name=systemd /container-cgroup
mkdir /container-cgroup/lxc
echo 1 > /container-cgroup/lxc/cgroup.procs

umount /sys/fs/cgroup/systemd/lxc
mount --bind /container-cgroup/lxc /sys/fs/cgroup/systemd/lxc

