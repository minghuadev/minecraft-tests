#!/bin/bash

# must have arm tool chain installed at $ARMTOOLSPATH:
if [ ! -f $ARMTOOLSPATH/arm-none-linux-gnueabi-gcc ]; then
    echo No gcc found at $ARMTOOLSPATH/arm-none-linux-gnueabi-gcc
    echo Must set ARMTOOLSPATH so a gcc is at \$ARMTOOLSPATH/arm-none-linux-gnueabi-gcc
    exit 1
fi
    # example toolchain: see http://elinux.org/ARMCompilers
    #   https://sourcery.mentor.com/GNUToolchain/package12774/public/arm-none-eabi/arm-2014.05-28-arm-none-eabi-i686-pc-linux-gnu.tar.bz2
    #   https://sourcery.mentor.com/GNUToolchain/package12813/public/arm-none-linux-gnueabi/arm-2014.05-29-arm-none-linux-gnueabi-i686-pc-linux-gnu.tar.bz2


# change these to match your environment
TARGET_HOST="arm-none-linux-gnueabi"
CROSS_TOOLS_PATH=$ARMTOOLSPATH
BUILD_HOST="x86_64-linux-gnu"


# you shouldn't need to change these
PYTHON="Python-2.7.3"
CONFIGURE_ARGS="--disable-ipv6"
BUILD_LOG="build.log"

# build log goes here
rm -f $BUILD_LOG
touch $BUILD_LOG
echo "Build output will be in $BUILD_LOG"

# download dist if it doesn't already exist
if [ ! -f $PYTHON.tar.xz ] ; then
    echo "Downloading $PYTHON .."
    wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tar.xz >> $BUILD_LOG
fi

myskip=0
if [ -f $PYTHON/myskipdone1 ]; then 
myskip=1
  if [ -f $PYTHON/myskipdone2 ]; then 
  myskip=2
  fi
fi
mystatic=0
    # set mystatic to 1 to build non-static binary that is necessary for armv7
    # though armv5 may be able to build static , not sure how to do it ...

if [ $myskip -lt 1 ]; then
  rm -rf $PYTHON
  tar -xf $PYTHON.tar.xz
  cp -p files/config.site $PYTHON
fi
cd $PYTHON
BUILD_LOG="../$BUILD_LOG"
unset CROSS_COMPILE

# ensure static glibc is installed
rpm -qa | grep -q glibc-static
if [ $? -eq 1 ] ; then
    echo "Installing glibc-static (with sudo yum install) .."
    #sudo yum install -y glibc-static >> $BUILD_LOG
fi

set -e

# first we need to build the host executables (python and Parser/pgen)
if [ $myskip -lt 1 ]; then

  echo "Stage 1: compiling host executables .."

  echo >> $BUILD_LOG
  echo "Stage 1: compiling host executables .." >> $BUILD_LOG
  echo >> $BUILD_LOG

  ./configure $CONFIGURE_ARGS CFLAGS="-Wformat" CONFIG_SITE="config.site" >> $BUILD_LOG
  make python Parser/pgen >> $BUILD_LOG
  mv python hostpython
  mv Parser/pgen Parser/hostpgen
  make distclean
fi

# set up environment for cross compile - we really shouldn't blindly add to PATH
export PATH="$PATH:$CROSS_TOOLS_PATH"
export CROSS_COMPILE=${TARGET_HOST}-



if [ $myskip -lt 1 ]; then

  echo "Stage 1.5: patching Python for cross-compile .."

  echo >> $BUILD_LOG
  echo "Stage 1.5: patching Python for cross-compile .." >> $BUILD_LOG
  echo >> $BUILD_LOG

  patch -p0 < ../files/Python-2.7.3-xcompile.patch
fi

# cross compile
echo "Stage 2: configure cross-compiling for $TARGET_HOST from $BUILD_HOST .."

echo >> $BUILD_LOG
echo "Stage 2: configure cross-compiling for $TARGET_HOST from $BUILD_HOST .." >> $BUILD_LOG
echo >> $BUILD_LOG

if [ $myskip -lt 2 ]; then
  if [ $mystatic -ne 1 ]; then

    if [ -f Makefile ]; then make distclean ; fi
    ./configure $CONFIGURE_ARGS  --build=$BUILD_HOST --host=$TARGET_HOST \
       CFLAGS="-Wformat" LDFLAGS="-static -static-libgcc" CPPFLAGS="-static" \
       CONFIG_SITE="config.site" >> $BUILD_LOG
    rm -f myskipdone3 myskipdone4
  else

    if [ -f Makefile ]; then make distclean ; fi
    ./configure $CONFIGURE_ARGS --build=$BUILD_HOST --host=$TARGET_HOST \
       CFLAGS="-Wformat" CONFIG_SITE="config.site" --prefix=/python >> $BUILD_LOG
    rm -f myskipdone3 myskipdone4
  fi
  touch myskipdone2
fi

    function enable_modules() {
        for x in `cat << allines
          array
          cmath
          math
          _struct
          time
          operator
          _random
          _collections
          itertools
          strop
          _functools
          _elementtree
          datetime
          _bisect
        
          unicodedata
        
          fcntl
          spwd
          grp
          select
        
          _socket
        
          binascii
          cStringIO
        
          _md5 
          _sha 
          _sha256
          _sha512 `; do 
        
            echo "  " Enable builtin module: $x
            echo "  " Enable builtin module: $x >> $BUILD_LOG
            sed -e "s/^#\($x[ \t].*\)$/\1/" -i Modules/Setup
        done
    }

if [ $myskip -lt 1 ]; then
  if [ $mystatic -ne 1 ]; then
    sed -i '1r ../files/Setup' Modules/Setup
    echo
    echo "Touching Modules/Setup"
    echo "Touching Modules/Setup" >> $BUILD_LOG
    enable_modules
    echo
  else
    echo
    echo "Skip touching Modules/Setup for static"
    echo "Skip touching Modules/Setup for static" >> $BUILD_LOG
    echo
  fi
  touch myskipdone1
else
  if [ $mystatic -ne 1 ]; then
    set +e
    grep '^\*static\*' Modules/Setup
    rc33=$?
    set -e
    if [ $rc33 -ne 0 ]; then 
      sed -i '1r ../files/Setup' Modules/Setup
      echo
      echo "Touching Modules/Setup"
      echo "Touching Modules/Setup" >> $BUILD_LOG
      enable_modules
      echo
    fi
  else 
    echo
    echo "Skip touching Modules/Setup"
    echo "Skip touching Modules/Setup" >> $BUILD_LOG
    echo
  fi
fi

if [ -f myskipdone3 ]; then
  echo
  echo "Skip Stage 3: cross-compiling make"
  echo
else

  echo "Stage 3: cross-compiling make for $TARGET_HOST .."

  echo >> $BUILD_LOG
  echo "Stage 3: cross-compiling make for $TARGET_HOST .." >> $BUILD_LOG
  echo >> $BUILD_LOG
  
  if [ $mystatic -ne 1 ]; then
    # static build, make for target python only. 
    make python HOSTPYTHON=./hostpython HOSTPGEN=./Parser/hostpgen \
      CROSS_COMPILE_TARGET=yes BUILDARCH=$BUILD_HOST HOSTARCH=$TARGET_HOST >> $BUILD_LOG  2>&1 
    rc3=$?
  else
    make HOSTPYTHON=./hostpython HOSTPGEN=./Parser/hostpgen \
      BLDSHARED="${CROSS_COMPILE}gcc -shared" \
      CROSS_COMPILE_TARGET=yes BUILDARCH=$BUILD_HOST HOSTARCH=$TARGET_HOST >> $BUILD_LOG  2>&1 
    rc3=$?
  fi
  
  sed -n -e '/Python build finished/,$p' $BUILD_LOG | grep -v 'install'
  file python
  
  if [ $rc3 -eq 0 ]; then
    touch myskipdone3
  fi

fi


if [ -f myskipdone4 ]; then
  echo
  echo "Skip Stage 4: cross-compiling make install"
  echo
else
  echo "Stage 4: cross-compiling make install for $TARGET_HOST .."

  echo >> $BUILD_LOG
  echo "Stage 4: cross-compiling make install for $TARGET_HOST .." >> $BUILD_LOG
  echo >> $BUILD_LOG

  myinstalldir=`pwd`/_install
  echo >> $BUILD_LOG
  echo "State 4 install to $myinstalldir"
  echo "State 4 install to $myinstalldir" >> $BUILD_LOG
  echo >> $BUILD_LOG

  if [ $mystatic -ne 1 ]; then
    echo
    echo >> $BUILD_LOG
    echo "Skip Stage 4: cross-compiling make install for static"
    echo "Skip Stage 4: cross-compiling make install for static" >> $BUILD_LOG
    echo
    echo >> $BUILD_LOG

    #make install HOSTPYTHON=./hostpython  \
    #  CROSS_COMPILE_TARGET=yes prefix=$myinstalldir  >> $BUILD_LOG  2>&1 
    #rc4=$?
    #if [ $rc4 -eq 0 ]; then
    #   touch myskipdone4
    #fi

  else
    make install HOSTPYTHON=./hostpython  \
      BLDSHARED="${CROSS_COMPILE}gcc -shared" \
      CROSS_COMPILE_TARGET=yes prefix=$myinstalldir  >> $BUILD_LOG  2>&1 
    rc4=$?
    if [ $rc4 -eq 0 ]; then
       touch myskipdone4
    fi
  fi
fi


