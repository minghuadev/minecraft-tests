#!/bin/bash
# dkf4.bash

curr_uid=`id -u`
curr_gid=`id -g`

rm the.dockerfile

cat << EOF_DOCKERFILE > the.dockerfile
 FROM ubuntu:trusty-20181115

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

 USER \$USERNAME
 CMD /bin/bash
EOF_DOCKERFILE

echo; echo build dkf4.img
docker build --build-arg UID=${curr_uid} --build-arg GID=${curr_gid} \
    -f the.dockerfile -t dkf4.img .
echo; echo build dkf4.img done


#docker run -td \
#    -v $(pwd)/sharedfolder:/home/hdler/sharedfolder \
#    --name dkf4 dkf4.img


#extra packages: gperf texinfo wget gawk libtool automake 
#  zlib-bin zlib1g-dev

[EXTRA]  Saving state to restart at step 'cc_core_pass_1'...
[INFO ]  =================================================================
[INFO ]  Installing pass-1 core C compiler
[EXTRA]    Configuring gcc
[EXTRA]    Building gcc
[ERROR]    checking dynamic linker characteristics... configure: error: Link tests are not allowed after GCC_NO_EXECUTABLES.
[ERROR]    make[2]: *** [configure-zlib] Error 1
[ERROR]
[ERROR]  >>
[ERROR]  >>  Build failed in step 'Installing pass-1 core C compiler'
[ERROR]  >>        called in step '(top-level)'
[ERROR]  >>
[ERROR]  >>  Error happened in: CT_DoExecLog[scripts/functions@257]
[ERROR]  >>        called from: do_cc_core_backend[scripts/build/cc/gcc.sh@455]
[ERROR]  >>        called from: do_cc_core_pass_1[scripts/build/cc/gcc.sh@101]
[ERROR]  >>        called from: main[scripts/crosstool-NG.sh@632]


Current command:
  'make' '-j1' '-l' 'all-gcc'
exited with error code: 2
Please fix it up and finish by exiting the shell with one of these values:
    1  fixed, continue with next build command
    2  repeat this build command
    3  abort build

ct-ng:~/sharedfolder/crosstool-ng/targets/microblaze-xilinx-elf/build/build-cc-core-pass-1>

[INFO ]  Installing binutils for host: done in 351.02s (at 08:00)
[EXTRA]  Saving state to restart at step 'cc_core_pass_1'...
[INFO ]  =================================================================
[INFO ]  Installing pass-1 core C compiler
[EXTRA]    Configuring gcc
[EXTRA]    Building gcc
[ERROR]    /home/hdler/sharedfolder/crosstool-ng/targets/src/gcc-custom/gcc/lto-compress.c:34:18: fatal error: zlib.h: No such file or directory
[ERROR]    make[3]: *** [lto-compress.o] Error 1
[ERROR]    make[2]: *** [all-gcc] Error 2
[ERROR]
[ERROR]  >>
[ERROR]  >>  Build failed in step 'Installing pass-1 core C compiler'
[ERROR]  >>        called in step '(top-level)'
[ERROR]  >>
[ERROR]  >>  Error happened in: CT_DoExecLog[scripts/functions@257]
[ERROR]  >>        called from: do_cc_core_backend[scripts/build/cc/gcc.sh@455]
[ERROR]  >>        called from: do_cc_core_pass_1[scripts/build/cc/gcc.sh@101]
[ERROR]  >>        called from: main[scripts/crosstool-NG.sh@632]


Current command:
  'make' '-j1' '-l' 'all-gcc'
exited with error code: 2
Please fix it up and finish by exiting the shell with one of these values:
    1  fixed, continue with next build command
    2  repeat this build command
    3  abort build

ct-ng:~/sharedfolder/crosstool-ng/targets/microblaze-xilinx-elf/build/build-cc-core-pass-1> exit 2
exit

Re-trying last command.


