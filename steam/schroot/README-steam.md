
gui app
=============

reference: http://repo.steampowered.com/steam/archive/precise/
wget http://repo.steampowered.com/steam/archive/precise/steam_1.0.0.49.tar.gz
yum install xz
untar into ~/bin

run
    bin/steam/steam

it prompts
    installs into ~/.local/share/Steam
    STEAM_RUNTIME ...: /home/steamer/.local/share/Steam/ubuntu12_32/steam-runtime
    /home/steamer/.local/share/Steam/steam.sh: line 327: zenity: command not found

change app location: 
    menu Steam/Settings
    choose Downloads/Content Libraries/STEAM LIBRARY FOLDERS
    add a folder ~/apps

install civ v, and select location to install in the diaglog.



command line app
==================

reference: https://developer.valvesoftware.com/wiki/SteamCMD

cd
mkdir bin
mkdir apps
cd bin
wget http://media.steampowered.com/installer/steamcmd_linux.tar.gz
tar zxf steamcmd_linux.tar.gz

cd ../apps
../bin/steamcmd.sh



