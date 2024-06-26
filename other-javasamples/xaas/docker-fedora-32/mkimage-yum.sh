#!/usr/bin/env bash
#
# Create a base CentOS Docker image.
#
# This script is useful on systems with yum installed (e.g., building
# a CentOS image on CentOS).  See contrib/mkimage-rinse.sh for a way
# to build CentOS images on other systems.

usage() {
    cat <<EOOPTS
$(basename $0) [OPTIONS] <name> [repo name]
OPTIONS:
  -y <yumconf>  The path to the yum config to install packages from. The
                default is /etc/yum/yum.conf.
  -m <maintainer>  The maintainer to use
                default is "Me <me@mail.com>".

EOOPTS
    exit 1
}

# option defaults
yum_config=/etc/yum/yum.conf
maintainer="Me <me@mail.com>"
while getopts ":y:m:h" opt; do
    case $opt in
        y)
            yum_config=$OPTARG
            ;;
        m)
            maintainer=$OPTARG
            ;;
        h)
            usage
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            usage
            ;;
    esac
done
shift $((OPTIND - 1))
name=$1

if [[ -z $name ]]; then
    usage
fi

repo_name=$2
if [[ -z $repo_name ]]; then
    repo_name=$name
fi

#--------------------

target=$(mktemp -d --tmpdir $(basename $0).XXXXXX)

set -x

mkdir -m 755 "$target"/dev
mknod -m 600 "$target"/dev/console c 5 1
mknod -m 600 "$target"/dev/initctl p
mknod -m 666 "$target"/dev/full c 1 7
mknod -m 666 "$target"/dev/null c 1 3
mknod -m 666 "$target"/dev/ptmx c 5 2
mknod -m 666 "$target"/dev/random c 1 8
mknod -m 666 "$target"/dev/tty c 5 0
mknod -m 666 "$target"/dev/tty0 c 4 0
mknod -m 666 "$target"/dev/urandom c 1 9
mknod -m 666 "$target"/dev/zero c 1 5

# amazon linux yum will fail without vars set
if [ -d /etc/yum/vars ]; then
	mkdir -p -m 755 "$target"/etc/yum
	cp -a /etc/yum/vars "$target"/etc/yum/
fi

yum -c "$yum_config" --installroot="$target" --releasever=/ --setopt=tsflags=nodocs \
    --setopt=group_package_types=mandatory -y groupinstall Core
yum -c "$yum_config" --installroot="$target" -y clean all

cat > "$target"/etc/sysconfig/network <<EOF
NETWORKING=yes
HOSTNAME=localhost.localdomain
EOF

# effectively: febootstrap-minimize --keep-zoneinfo --keep-rpmdb
# --keep-services "$target".  Stolen from mkimage-rinse.sh
#  locales
rm -rf "$target"/usr/{{lib,share}/locale,{lib,lib64}/gconv,bin/localedef,sbin/build-locale-archive}
#  docs
rm -rf "$target"/usr/share/{man,doc,info,gnome/help}
#  cracklib
rm -rf "$target"/usr/share/cracklib
#  i18n
rm -rf "$target"/usr/share/i18n
#  sln
rm -rf "$target"/sbin/sln
#  ldconfig
rm -rf "$target"/etc/ld.so.cache
rm -rf "$target"/var/cache/ldconfig/*

version=
for file in "$target"/etc/{redhat,system}-release
do
    if [ -r "$file" ]; then
        version="$(sed 's/^[^0-9\]*\([0-9.]\+\).*$/\1/' "$file")"
        break
    fi
done

if [ -z "$version" ]; then
    echo >&2 "warning: cannot autodetect OS version, using '$name' as tag"
    version=$name
fi

#tar --numeric-owner -c -C "$target" . | docker import - $name:$version
#docker run -i -t $name:$version echo success

tmp_build=$(mktemp -d --tmpdir $(basename $0).XXXXXX)
tar --numeric-owner -c  -J -f "$tmp_build/$name-$version-docker.tar.xz" -C "$target" .

rm -rf "$target"

echo "FROM scratch" > "$tmp_build/Dockerfile"
echo "MAINTAINER $maintainer" >> "$tmp_build/Dockerfile"
echo "ADD $name-$version-docker.tar.xz /" >> "$tmp_build/Dockerfile"
echo "LABEL Vendor=\"Fedora\"" >> "$tmp_build/Dockerfile"
echo "LABEL License=GPLv2" >> "$tmp_build/Dockerfile"
echo "" >> "$tmp_build/Dockerfile"
echo "# Volumes for systemd" >> "$tmp_build/Dockerfile"
echo "# VOLUME ["/run", "/tmp"]" >> "$tmp_build/Dockerfile"
echo "" >> "$tmp_build/Dockerfile"
echo "# Environment for systemd" >> "$tmp_build/Dockerfile"
echo "# ENV container=docker" >> "$tmp_build/Dockerfile"
echo "" >> "$tmp_build/Dockerfile"
echo "# For systemd usage this changes to /usr/sbin/init" >> "$tmp_build/Dockerfile"
echo "# Keeping it as /bin/bash for compatability with previous" >> "$tmp_build/Dockerfile"
echo "CMD [\"/bin/bash\"]" >> "$tmp_build/Dockerfile"

docker build -t "$repo_name:$version" "$tmp_build"

rm -rf "$tmp_build"

docker run "$repo_name:$version" echo "Works!"


