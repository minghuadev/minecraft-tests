

follow ../lxc-lxd-docs/readme-steam-3-lxd


softlink ~/vshare3/local-share to ~/.local/share


run steam in user ubuntu to install  
  The packages cache seems to be out of date
  Press return to update the list of available packages: 
  it asks for authentication to run /usr/bin/steamdeps ... , 

  https://stackoverflow.com/questions/62520049/how-to-get-steam-to-run-on-ubuntu-20-04
  run 
        STEAM_RUNTIME=0 steam
  to find out the missing depencies and install them manually.
        You are missing the following 32-bit libraries, and Steam may not run:
        libGL.so.1 libXtst.so.6 libXfixes.so.3 libXrandr.so.2
        libXrender.so.1 libXext.so.6 libXi.so.6 libgobject-2.0.so.0
        libglib-2.0.so.0 libgio-2.0.so.0 libgtk-x11-2.0.so.0 libpipewire-0.3.so.0
        libpulse.so.0 libgdk_pixbuf-2.0.so.0 libxcb-res.so.0 libva.so.2
        libvdpau.so.1 libva.so.2 libbz2.so.1.0

  manually install: 
        libgl1:i386 libxtst6:i386 libxrandr2:i386 libxi6:i386 
        libglib2.0-0:i386 libgtk2.0-0:i386 libpulse0:i386 libxcb-res0:i386
        libva2:i386 libbz2-1.0:i386
        libpipewire-0.3-0:i386 libvdpau1:i386

  run again, it prompts need to install these packages: manually install them
        libc6:amd64 libc6:i386 libegl1:amd64 libegl1:i386 libgbm1:amd64 
        libgbm1:i386 libgl1-mesa-dri:amd64 libgl1-mesa-dri:i386 libgl1:amd64 
        libgl1:i386 steam-libs-amd64:amd64 steam-libs-i386:i386
  the steam-libs-amd64:amd64 and steam-libs-i386:i386 could not be found.
  it's possible that these are due to not installing steam.deb, 
  thus wget and install steam.deb as in the document ../lxc-lxd-docs/readme-3...,
  then install these packages again.

restart the container.
login using 
        lxc exec steam3-ubuntu -- sudo --user ubuntu --login

soft link ~/.local/share
run steam

  previous error: 
        got a failure and notice to visit: 
        https://support.steampowered.com/kb_article.php?ref=9205-OZVN-0660

  previous error without security nesting: 

        the sreen error: 
        [2023-08-26 04:22:40] Verification complete
        src/steamUI/Main.cpp (3174) : !"Fatal Error: Could not load module 'bin/vgui2_s.dll'"
        https://github.com/ValveSoftware/steam-for-linux/issues/9198
            cd ~/.local/share/Steam/ubuntu12_32
            LD_LIBRARY_PATH="$LD_LIBRARY_PATH:." ./steam-runtime/run.sh ldd vgui2_s.so

  errors: 
    first time error
        a white window at screen center
    run with runtime disabled: 
        will hit the fatal not loading bin/vgui2_s.dll error

    search  steam linux how to run the runtime
    search  steam linux empty lauch window
    https://github.com/ValveSoftware/steam-for-linux/issues/9386

    search steam linux login window blank
    https://github.com/ValveSoftware/steam-for-linux/issues/9234
        check cef_log.txt, steamwebhelper.log, webhelper.txt

    search steam linux uncaught in promise typeerror
    https://github.com/ValveSoftware/steam-for-linux/issues/9780
        command line options: -offline, --reset, -cef-disable-gpu, -bigpicture
        workaround: -vgui
    https://github.com/ValveSoftware/steam-for-linux/issues/9783
    https://github.com/ValveSoftware/steam-for-linux/issues/9752
        workaround: install steamcmd, install game, login
      caused by sdl 
        https://github.com/libsdl-org/SDL/issues/7975
          https://gitlab.freedesktop.org/mesa/mesa/-/issues/9345
              the following show show a llvmpipe
              glxinfo | grep renderer

    https://developer.valvesoftware.com/wiki/SteamCMD#With_a_Steam_Account

    search steam linux client roll back to previous version
    https://steamcommunity.com/discussions/forum/0/6516193260168294059/
    Solution: To Revert To Old UI

        add this to the command line: 
            -forcesteamupdate -forcepackagedownload -overridepackageurl http://web.archive.org/web/20230531113527if_/media.steampowered.com/client -exitsteam
        create a file "steam.cfg" in the steam main folder to have: 

            BootStrapperInhibitAll=Enable
            BootStrapperForceSelfUpdate=False

        for linux, use this after the web/ : 20230531115543
        full command line: 

            steam -forcesteamupdate -forcepackagedownload -overridepackageurl http://web.archive.org/web/20230531115543if_/media.steampowered.com/client -exitsteam

        then can run steam with -offline -vgui options.
        ok without those two options on the ubuntu23 lxc container.



