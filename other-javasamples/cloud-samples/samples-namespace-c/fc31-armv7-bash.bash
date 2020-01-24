#!/bin/bash

# retrieve arch from a rpm package file: 
# https://unix.stackexchange.com/questions/328720/how-to-extract-the-instructions-provided-by-the-rpm-spec-file
#   rpm -qp --queryformat '%{ARCH} %{NAME}\n' (if you have an RPM file)

repotrack \
    -c $HOME/repoconf/yum.conf \
    -a armv7hl  \
    -r fc31arm32upd \
    --repofrompath=fc31arm32upd,https://mirrors.kernel.org/fedora/updates/31/Everything/armhfp \
    -r fc31arm32os \
    --repofrompath=fc31arm32os,https://mirrors.kernel.org/fedora/releases/31/Everything/armhfp/os \
    -p $HOME/repolocal/repodest-f31bash  \
    bash

#    strace
#    python

