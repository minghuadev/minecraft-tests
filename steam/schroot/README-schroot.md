

chroot fedora 21 i386 system
=============================


base guest system install from the host
----------------------------------------

    $ wget http://mirrors.kernel.org/fedora/releases/21/Everything/i386/os/Packages/f/fedora-release-21-2.noarch.rpm
    $ wget http://mirrors.kernel.org/fedora/releases/21/Everything/i386/os/Packages/f/fedora-repos-21-2.noarch.rpm

    # rpm --root /opt/svr --initdb
    # rpm --root /opt/svr -i fedora-release-21-2.noarch.rpm fedora-repos-21-2.noarch.rpm

May need the key for installing rawhind (don't if it does not complain):
    # rpm --root /opt/svr --import https://fedoraproject.org/static/246110C1.txt

    # yum --installroot=/opt/svr install yum bash net-tools iputils tar passwd


host schroot setup
-------------------

Create a host user acocunt "steamer".

Use "sciv" as schroot name. 

Edit /etc/schroot/schroot.conf, add this: 

    [sciv]
    description=Debian sciv (unstable)
    directory=/opt/svr
    type=directory
    users=steamer
    groups=steamer
    root-groups=root
    aliases=unstablesciv,defaultsciv

On x64 host, add "personality=linux32" too.

Edit /etc/schroot/default/copyfiles. Leave only this:
 
    /etc/resolv.conf

Edit /etc/schroot/default/nssdatabases, comment out all the lines.

Edit /etc/schroot/default/fstab. Comment out all lines except for : 

    /proc  /sys  /dev  /dev/pts  /dev/shm

Copy the lines for use "steamer" from /etc/{passwd,group} to /opt/svr/etc/{passwd,group}.

Edit /opt/srv/etc/shadow to remove the root password:

    #root:*:16229:0:99999:7:::
    root::16229:0:99999:7:::

Create the home folder for user "steamer" of the guest os: 

    # mkdir /opt/svr/home/steamer
    # chown steamer:steamer /opt/svr/home/steamer


guest os firstboot setup
-------------------------

On host, get into "steamer" user account:
    $ su - steamer

Verify x display on the host:
    $ xterm
    $ glxgears

Get into chroot guest os and setup root password (in the guest the /opt is empty), 
and verify network is working:
    $ schroot -c sciv
    $ ls /opt
    $ su
    # passwd
    # exit
    $ ping www.google.com

Exit from the chroot: 
    $ exit


guest os package setup
-----------------------

Allow guest os to send x display to the host, on the host run:
    $ xhost +

Get into the guest os. Install packages:
    $ yum install which vi findutils
    $ yum install procps-ng xz
    $ yum install xterm
    $ yum install glx-utils
    # yum install mesa-dri-drivers

Verify x and glx:
    $ export DISPLAY=:0.0
    $ xterm
    $ glxgears

Add "export DISPLAY=:0.0" to ~/.bash_profile .
Add user "steamer" to the "video" group so it can access /dev/dri/card0. 
Run "su - steamer" so the group identity takes effect each time getting into schroot guest.


guest os dri debug
-----------------------

Verify hardware dri is used: 
    $ glxinfo | grep OpenGL

Check which dri card and driver is used (on host and guest):
    $ glxgears &
    $ ps | grep glxgears
    $ pmap -p <glxgears-pid> | grep dri

The output of pmap should contain, e.g. :
    75000     55K rw-s- /dev/dri/card0
    77000   3333K r-x-- /usr/lib/dri/i340_dri.so

Or if software rendering is used, that is not right:
    77000   8888K r-x-- /usr/lib/dri/swrast_dri.so

Verify the permission to write to /dev/dri/card0: 
    $ echo 12345 > /dev/dri/card0


guest os fonts
------------------------------------------------

yum install xorg-x11-fonts-ISO8859-1-100dpi
yum install  gnu-free-fonts-common
yum install  gnu-free-mono-fonts
yum install  gnu-free-sans-fonts
yum install  gnu-free-serif-fonts


