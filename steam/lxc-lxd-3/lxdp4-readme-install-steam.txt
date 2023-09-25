

follow ../lxc-lxd-docs/readme-steam-3-lxd

N: Download is performed unsandboxed as root as file '/root/steam.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)

chown _apt /root/steam.deb

install again, no change


run steam in user ubuntu to install  
  The packages cache seems to be out of date
  Press return to update the list of available packages: 
  it asks for authentication to run /usr/bin/steamdeps ... , 

  https://stackoverflow.com/questions/62520049/how-to-get-steam-to-run-on-ubuntu-20-04
  run 
        STEAM_RUNTIME=0 steam
  to find out the missing depencies and install them manually.
        You are missing the following 32-bit libraries, and Steam may not run:
        libGL.so.1
        libXtst.so.6
        libXfixes.so.3
        libXrandr.so.2
        libXrender.so.1
        libXext.so.6
        libX11.so.6
        libXi.so.6
        libgobject-2.0.so.0
        libglib-2.0.so.0
        libgio-2.0.so.0
        libgtk-x11-2.0.so.0
        libpipewire-0.3.so.0
        libpulse.so.0
        libgdk_pixbuf-2.0.so.0
        libxcb-res.so.0
        libva.so.2
        libvdpau.so.1
        libX11.so.6
        libva.so.2
        libbz2.so.1.0

  manually install: 
        libgl1:i386 libxtst6:i386 libxrandr2:i386 libxi6:i386 
        libglib2.0-0:i386 libgtk2.0-0:i386 libpulse0:i386 libxcb-res0:i386
        libva2:i386 libbz2-1.0:i386

  still missing libpipewire and libvdpau. package search found in 22.04 jammy

  https://bugs.launchpad.net/ubuntu/+source/pipewire/+bug/1931312
  libpipewire-0.3-0

Package libegl1:i386 needs to be installed
Package libgbm1:i386 needs to be installed
Package steam-libs-amd64:amd64 needs to be installed
Package steam-libs-i386:i386 needs to be installed
Package xdg-desktop-portal needs to be installed
Package xdg-desktop-portal-gtk needs to be installed


runs out of space. 
soft link ~/vshare3/local-share/ to ~/.local/share/


