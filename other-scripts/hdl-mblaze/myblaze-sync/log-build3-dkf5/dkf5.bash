#!/bin/bash
# dkf5.bash

curr_uid=`id -u`
curr_gid=`id -g`

rm the.dockerfile

cat << EOF_DOCKERFILE > the.dockerfile
 #FROM ubuntu:trusty-20181115
 FROM ubuntu:bionic-20181112

 ARG USERNAME=hdler
 ARG UID=1999
 ARG GID=1999

 RUN groupadd -g \$GID \$USERNAME
 RUN useradd -m -u \$UID -g \$GID -s /bin/bash \$USERNAME

 RUN rm /bin/sh && ln -s bash /bin/sh
 RUN cp -a /etc /etc-original && chmod a+rw /etc

 RUN apt-get update
 RUN apt-get install -y git tree openssh-client make
 RUN apt-get install -y bzip2 gcc bc file vim 
 RUN apt-get install -y libncurses5-dev pkg-config bison flex
 RUN apt-get install -y build-essential
 RUN apt-get install -y gperf texinfo wget gawk libtool automake
 RUN apt-get install -y zlib1g-dev

 USER \$USERNAME
 CMD /bin/bash
EOF_DOCKERFILE

echo; echo build dkf5.img
docker build --build-arg UID=${curr_uid} --build-arg GID=${curr_gid} \
    -f the.dockerfile -t dkf5.img .
echo; echo build dkf5.img done


#docker run -td \
#    -v $(pwd)/sharedfolder:/home/hdler/sharedfolder \
#    --name dkf5 dkf5.img


