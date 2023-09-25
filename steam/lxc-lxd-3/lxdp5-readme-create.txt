
reference: lxc-lxd-docs/readme-steam-2-gui
           lxc-lxd-docs2/readme-general-1-lxd-gui-profile

           https://www.funtoo.org/Steam/LXD


  copy lxdp3.txt to lxdp4.txt and change the name, share directory.
  create the host shared directory. 

  copy lxdp4.txt to lxdp5.txt and modify.

  create a new pool: do this once
    $ lxc storage create pool3 dir source=~/vshare3/root-pool
   or delete it and create it again to clean up


  launch: 

    $ lxc profile create gui3
    $ cat lxdp5.txt | lxc profile edit gui3
    $ lxc launch --profile default --profile gui3 -s pool3 ubuntu:lunar -c security.nesting=true steam3-ubuntu

  exam: 
    $ lxc exec steam3-ubuntu -- sudo --user ubuntu --login

    ubuntu@gui2-ubuntu:~$ tail -6 /var/log/cloud-init.log
    ubuntu@gui2-ubuntu:~$ glxgears
    ubuntu@gui2-ubuntu:~$ pactl info


before creating new

$ lxc profile list
+-----------+---------------------+---------+
|   NAME    |     DESCRIPTION     | USED BY |
+-----------+---------------------+---------+
| default   | Default LXD profile | 2       |
+-----------+---------------------+---------+
| gui       | GUI LXD profile     | 0       |
+-----------+---------------------+---------+
| guishare  | GUI LXD profile     | 1       |
+-----------+---------------------+---------+
| guishare2 | GUI LXD profile     | 1       |
+-----------+---------------------+---------+

$ lxc list
+--------------+---------+----------------------+-----------------------------------------------+-----------+-----------+
|     NAME     |  STATE  |         IPV4         |                     IPV6                      |   TYPE    | SNAPSHOTS |
+--------------+---------+----------------------+-----------------------------------------------+-----------+-----------+
| gui2-ubuntu  | STOPPED |                      |                                               | CONTAINER | 0         |
+--------------+---------+----------------------+-----------------------------------------------+-----------+-----------+
| steam-ubuntu | RUNNING | 10.56.152.224 (eth0) | fd42:1ede:f33a:f4a1:216:3eff:fe39:b331 (eth0) | CONTAINER | 0         |
+--------------+---------+----------------------+-----------------------------------------------+-----------+-----------+


