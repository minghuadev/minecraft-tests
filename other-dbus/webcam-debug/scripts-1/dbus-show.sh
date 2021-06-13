#!/bin/sh

    function get_process_pid() {
      dbus-send --system --type=method_call --print-reply --dest=org.freedesktop.DBus \
              / org.freedesktop.DBus.GetConnectionUnixProcessID string:$1 2>/dev/null | \
          grep uint32 | sed -e 's/.*uint32 //' | xargs
    }

    function get_all_names() {
      #       string "org.freedesktop.DBus"
      dbus-send --system --type=method_call --print-reply --dest=org.freedesktop.DBus \
              /org/freedesktop/DBus org.freedesktop.DBus.ListNames | \
          grep 'string "' | sed -e 's/.*string "//' | sed -e 's/".*//'
    }

    function get_names_pids() {
        all_names=`get_all_names | xargs`
        for x in ${all_names} ; do
            # check if x == ':1.23' and its length
            pat_match=0
            echo $x | grep '^:1\.' > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                pat_match=1
            fi
            pat_len=3 # default ok
            if [ $pat_match -eq 1 ]; then
                # should be 4 to 6, plus a trailing eol
                pat_len=`echo $x | wc -m`
            fi
            if [ $pat_len -gt 2 -a $pat_len -le 7 ]; then
                pid=`get_process_pid $x`
                pid_len=`echo $pid | wc -m`
                if [ $pid_len -ge 2 -a $pid_len -le 8 ]; then
                    echo ok name pid: $pid $x
                else
                    echo skip name: $x '  ' pid $pid
                fi
            else
                echo skip name: $x
            fi
        done
    }

get_names_pids | sort

# [root@webcam:/userdata]# sh dbus-show.sh | sort
# pid name pid: 493 org.freedesktop.DBus
# pid name pid: 519 :1.0
# pid name pid: 519 net.connman
# pid name pid: 528 :1.2
# pid name pid: 528 fi.w1.wpa_supplicant1
# pid name pid: 531 :1.1
# pid name pid: 531 org.freedesktop.Avahi
# pid name pid: 613 :1.6
# pid name pid: 613 webcam.system
# pid name pid: 620 :1.3
# pid name pid: 620 webcam.dbserver
# pid name pid: 626 :1.4
# pid name pid: 626 :1.5
# pid name pid: 626 webcam.netserver
# pid name pid: 633 :1.7
# pid name pid: 633 :1.8
# pid name pid: 633 webcam.StorageManager
# pid name pid: 669 :1.10
# pid name pid: 669 :1.9
# pid name pid: 669 webcam.ispserver
# pid name pid: 683 :1.11
# pid name pid: 683 :1.12
# pid name pid: 683 webcam.mediaserver.control
# skip name: :1.207

# [root@webcam:/userdata]# ps 493 519 528 531 613 620 626 633 669 683
#  PID TTY      STAT   TIME COMMAND
#  493 ?        Ss     0:47 dbus-daemon --system
#  519 ?        S      0:43 /usr/sbin/connmand -n
#  528 ?        S      0:52 /usr/sbin/wpa_supplicant -u
#  531 ?        S      0:01 avahi-daemon: running [webcam.local]
#  613 ?        S      0:52 ipc-daemon --no-mediaserver
#  620 ?        S      0:00 dbserver /data/sysconfig.db
#  626 ?        Sl     0:15 netserver
#  633 ?        Sl     0:06 storage_manager /data/file.db
#  669 ?        Sl   193:19 ispserver
#  683 ?        Sl   432:47 mediaserver -c /oem/usr/share/mediaserver/webcam/ipc.c

#processes and whether they are on dbus labeled below [dbus-yes]
# [root@webcam:/userdata]# ps -efHw
# UID       PID PPID  C STIME TTY          TIME CMD
# root        2    0  0 Dec12 ?        00:00:00 [kthreadd]
# root        3    2  0 Dec12 ?        00:00:00   [rcu_gp]
# ....
# root        1    0  0 Dec12 ?        00:00:00 init
# root      101    1  0 Dec12 ?        00:00:01   /sbin/syslogd -n
# root      104    1  0 Dec12 ?        00:00:00   /sbin/klogd -n
# root      111    1  0 Dec12 ?        00:00:00   /sbin/udevd -d
# dbus      493    1  0 Dec12 ?        00:00:47   dbus-daemon --system                          [dbus-yes]
# root      519    1  0 Dec12 ?        00:00:43   /usr/sbin/connmand -n                         [dbus-yes]
# root      528    1  0 Dec12 ?        00:00:52   /usr/sbin/wpa_supplicant -u                   [dbus-yes]
# avahi     531    1  0 Dec12 ?        00:00:01   avahi-daemon: running [webcam.local]    [dbus-yes]
# root      540    1  0 Dec12 ?        00:00:00   /usr/sbin/dropbear -R
# root      545    1  0 Dec12 ?        00:00:00   /usr/sbin/fcgiwrap -f -s unix:/run/fcgiwrap.sock
# root      551    1  0 Dec12 ?        00:00:00   nginx: master process /usr/sbin/nginx
# www-data  642  551  0 Dec12 ?        00:09:22     nginx: worker process
# root      588    1  0 Dec12 ?        00:00:06   /usr/bin/adbd
# root      799  588  0 Dec12 pts/0    00:00:00     /bin/sh -l
# root     2930  799  0 05:39 pts/0    00:00:00       ps -efHw
# root      607    1  0 Dec12 ?        00:00:00   /bin/sh /usr/bin/start_nn.sh
# root      660  607  3 Dec12 ?        00:31:10     nn_server
# root      613    1  0 Dec12 ?        00:00:52   ipc-daemon --no-mediaserver                   [dbus-yes]
# root      620    1  0 Dec12 ?        00:00:00   dbserver /data/sysconfig.db                   [dbus-yes]
# root      626    1  0 Dec12 ?        00:00:15   netserver                                     [dbus-yes]
# root      633    1  0 Dec12 ?        00:00:06   storage_manager /data/file.db                 [dbus-yes]
# root      669    1 18 Dec12 ?        03:13:41   ispserver                                     [dbus-yes]
# root      683    1 42 Dec12 ?        07:13:42   mediaserver -c /oem/usr/share/mediaserver/webcam/ipc.conf  [dbus-yes]
# root      704    1  0 Dec12 ?        00:00:00   input-event-daemon -v /dev/input/event0 /dev/input/event1

