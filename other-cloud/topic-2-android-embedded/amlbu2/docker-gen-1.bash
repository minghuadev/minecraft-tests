#!/bin/bash
# docker-gen.bash

# special suffix for user name and directories
#   e.g. "u7" will create:
#          amlu7       --docker guest user name
#          amlimgu7    --docker image name
#          amlbu7       --docker container name
ux="u2"


echo Creating bb.dockerfile ...

# create bb.dockerfile:
cat << EOF1 > bb.dockerfile

 #FROM ubuntu:focal-20210921 # focal fails aws_sdk build.
 FROM ubuntu:bionic-20210930

 RUN apt-get update
 RUN apt-get install -y git tree openssh-client make
 RUN apt-get install -y bzip2 gcc libncurses5-dev bc
 RUN apt-get install -y file vim
 RUN apt-get install -y zlib1g-dev g++
 RUN apt-get install -y libssl-dev

 # from "1.2.3 Installing the software package" of "Description of the installation"
 #RUN apt-get install -y make zlib1g-dev libncurses5-dev g++ bc libssl-dev 
 RUN apt-get install -y lib32z1 lib32stdc++6  ncurses-term libncursesw5-dev

 # tzdata
   ## preseed tzdata, update package index, upgrade packages and install needed software
   RUN truncate -s0 /tmp/preseed.cfg && \
       (echo "tzdata tzdata/Areas select America" >> /tmp/preseed.cfg) && \
       (echo "tzdata tzdata/Zones/America select Los_Angeles" >> /tmp/preseed.cfg) && \
       debconf-set-selections /tmp/preseed.cfg && \
       rm -f /etc/timezone /etc/localtime && \
       apt-get update && \
       DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true \
       apt-get install -y tzdata
   ## cleanup of files from setup
   RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

 # from "1.2.3 Installing the software package" of "Description of the installation"
 RUN apt-get update
 RUN apt-get install -y texinfo texlive gawk 

 # needed by wl18xx build
 RUN apt-get install -y autoconf libtool libglib2.0-dev bison flex

 # rk1808 96boards-tb-96aiot dependencies:
 RUN dpkg --add-architecture i386
 RUN apt-get update
 RUN DEBIAN_FRONTEND="noninteractive" TZ="America/Los_Angeles" apt-get install -y \
    git-core gitk git-gui gcc-arm-linux-gnueabihf u-boot-tools \
    device-tree-compiler gcc-aarch64-linux-gnu mtools parted libudev-dev libusb-1.0-0-dev \
    autoconf autotools-dev libsigsegv2 m4 \
    intltool libdrm-dev \
    curl sed \
    make binutils build-essential gcc g++ bash patch gzip bzip2 perl tar cpio python unzip \
    rsync file \
    bc wget libncurses5 \
    libglib2.0-dev libgtk2.0-dev libglade2-dev cvs git \
    mercurial rsync openssh-client subversion asciidoc w3m dblatex graphviz \
    libc6:i386 liblz4-tool \
    gawk

  # repo: removed to use a local copy
  # gawk: needed to build u-boot image.
  # libqt4-dev : removed for focal
  # python-linaro-image-tools linaro-image-tools : removed for focal
  # python-matplotlib : removed for focal

 # time needed for the rk1808 recovery build.sh script:
 RUN apt-get install -y time

 # unbuffer from expect and cmake needed by rv1126 build script:
 RUN apt-get update
 RUN apt-get install -y expect cmake

 ARG UNAME=aml${ux}

 ARG UID=9999
 ARG GID=9999

 RUN groupadd -g \$GID \$UNAME
 RUN useradd -m -u \$UID -g \$GID -s /bin/bash \$UNAME

 RUN rm /bin/sh && ln -s bash /bin/sh
 RUN cp -a /etc /etc-original && chmod a+rw /etc

 USER \$UNAME

 CMD /bin/bash
EOF1

set -ex

echo Docker build off bb.dockerfile ...
docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) \
     -f bb.dockerfile  -t amlimg${ux} .

echo Docker build finished ...


echo
echo Creating sh-create.bash file ...

cat << EOF2 > sh-create.bash
#!/bin/bash

if [ ! -d sharedfiles ]; then mkdir sharedfiles; fi
if [ ! -d buildfiles ]; then mkdir buildfiles; fi

    docker run -td \
         -v $(pwd)/sharedfiles:/home/aml${ux}/sharedfiles \\
         -v $(pwd)/buildfiles:/home/aml${ux}/buildfiles   \\
         --name amlb${ux}  amlimg${ux}

EOF2

echo Created sh-create.bash file ...


