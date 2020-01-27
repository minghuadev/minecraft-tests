#!/bin/bash

repotrack \
    -c $HOME/repoconf/yum.conf \
    -a armv7hl  \
    -r fc30arm32upd \
    --repofrompath=fc30arm32upd,https://mirrors.kernel.org/fedora/updates/30/Everything/armhfp \
    -r fc30arm32os \
    --repofrompath=fc30arm32os,https://mirrors.kernel.org/fedora/releases/30/Everything/armhfp/os \
    -p $HOME/repolocal/repodest-f30bash  \
    bash \
    coreutils \
    rpm \
    yum \
    fedora-release net-tools iputils \
    dnf

#    strace
#    python

