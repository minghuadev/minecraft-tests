#!/bin/bash
# dockerfile.bash

# current uid and gid 
curr_uid=`id -u` 
curr_gid=`id -g` 

echo Creating dockerfile.dockerfile ...

# create dockerfile.dockerfile:
cat << EOF1 > dockerfile.dockerfile

 FROM ubuntu:xenial-20201014

 RUN apt-get update
 RUN apt-get install -y git tree openssh-client make
 RUN apt-get install -y bzip2 gcc libncurses5-dev bc
 RUN apt-get install -y file vim
 RUN apt-get install -y zlib1g-dev g++
 RUN apt-get install -y libssl-dev
 # from "1.2.3 Installing the software package" of "Description of the installation 
 # and upgrade of the SDK.pdf", Issue 00B01 (2020-04-04)
 #RUN apt-get install -y make zlib1g-dev libncurses5-dev g++ bc libssl-dev 
 RUN apt-get install -y lib32z1 lib32stdc++6  ncurses-term libncursesw5-dev
 RUN apt-get install -y texinfo texlive gawk 

 RUN dpkg --add-architecture i386
 RUN apt-get update
 RUN apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 zlib1g:i386
 # from "1.2.3 Installing the software package"
 #RUN apt-get install -y libc6:i386 
 RUN apt-get install -y u-boot-tools:i386

 # needed by wl18xx build
 RUN apt-get install -y autoconf libtool libglib2.0-dev bison flex

 # needed by buildroot 2020.08.2
 RUN apt-get install -y cpio wget build-essential

 ARG UNAME=py3user

 ARG UID=9999
 ARG GID=9999

 RUN groupadd -g \$GID \$UNAME
 RUN useradd -m -u \$UID -g \$GID -s /bin/bash \$UNAME

 RUN rm /bin/sh && ln -s bash /bin/sh
 RUN cp -a /etc /etc-original && chmod a+rw /etc

 USER \$UNAME

 CMD /bin/bash
EOF1

echo Docker build off dockerfile.dockerfile ...
docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) \
     -f dockerfile.dockerfile  -t py3aarch64img .

echo Docker build finished ...

echo Creating sh-create.bash ...

# create sh-create.bash
cat << EOF2 > sh-create.bash
#!/bin/bash

if [ ! -d sharedfiles ]; then mkdir sharedfiles; fi
if [ ! -d buildfiles ]; then mkdir buildfiles; fi
if [ ! -d opt-hm-linux ]; then mkdir opt-hm-linux; fi

    docker run -td \
         -v $(pwd)/sharedfiles:/home/py3user/sharedfiles \
         -v $(pwd)/buildfiles:/home/py3user/buildfiles   \
         -v $(pwd)/opt-hm-linux:/opt/hm-linux          \
         --name py3build  py3aarch64img
EOF2


