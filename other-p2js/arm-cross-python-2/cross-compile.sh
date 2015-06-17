#!/bin/bash
# Define package and job specific values
cd `dirname "$0"`
JOBS=8
CWD=`pwd`
MYTOOL=`basename ${CWD}`
# We are building outside of LTIB with results to be merged into LTIB's rootfs
# This is the rootfs targer directory inside LTIB
export RFS="/local/my_root_file_system"

# Undo cross-compile environment variables, if set
unset ROOT
unset SDKDIR
unset KLIBDIR
unset NFSDIR
unset CONFIG
unset CONFIGURED
unset ARCH
unset OS
unset TOOLCHAIN_BASE
unset TOOLCHAIN_BIN
unset CROSS_COMPILE
unset c
unset KERNEL_DIR
unset AS
unset LD
unset CC
unset AR
unset STRIP
unset SSTRIP
unset OBJCOPY
unset OBJDUMP
unset MAKE
unset CFLAGS

# Make the python interpreter and Parser/pgen for the build-host
echo "(I) Configuring Python build for host."
make distclean
rm -rf python_for_build Parser/pgen_for_build
# restore unmodified versions, in case of crash in previous build
git checkout -- Makefile.pre.in Modules/Setup.dist configure setup.py
./configure
if [ $? != 0 ]; then
    echo "(E) Configuration of Python build for host failed."
    exit 1
fi
make --jobs=${JOBS} python Parser/pgen
if [ $? != 0 ]; then
    echo "(E) Compilation of Python and Parser/pgen for host failed."
    exit 2
fi
mv python python_for_build
mv Parser/pgen Parser/pgen_for_build

# dd the cross compile patches
echo "(I) Patching cross-compile Python build."
patch -p3 < Python-2.7.5-xcompile.patch

# Setup cross-compile environment
#Now, start building everything for the target
echo "(I) Reconfiguring build environment for cross-compile..."
export PATH="/opt/freescale/usr/local/gcc-4.3.74-eglibc-2.8.74-dp-2/powerpc-none-linux-gnuspe/bin:${PATH}"
make distclean

./configure --host=powerpc-none-linux-gnuspe --build=i586-linux-gnu --prefix=/	\
    --disable-ipv6 ac_cv_file__dev_ptmx=no ac_cv_file__dev_ptc=no ac_cv_have_long_long_format=yes

if [ $? != 0 ]; then
    echo "(E) Configuration FAILED!"
    exit 3
fi

echo "(I) Cross-compiling Python ..."
make --jobs=${JOBS} \
    CFLAGS="-g0 -Os -s -I${RFS}/usr/include -L${RFS}/usr/lib -L${RFS}/lib -fdata-sections -ffunction-sections" \
    LDFLAGS='-I${RFS}/usr/include -L${RFS}/usr/lib -L${RFS}/lib'
if [ $? != 0 ]; then
    echo "(E) Compilation FAILED!"
    exit 4
fi

echo "(I) Stripping Python binary ..."
powerpc-none-linux-gnuspe-strip --strip-unneeded python

echo "(I) Installing Python ..."
sudo make install DESTDIR=${RFS} PATH="${PATH}"
if [ $? != 0 ]; then
    echo "(E) Installation FAILED!"
    exit 5
fi

echo "(I) Python cross-compilation and installation is done!"
# restore unpatched versions, so git does not complain about modified files
git checkout -- Makefile.pre.in Modules/Setup.dist configure setup.py
exit 0
