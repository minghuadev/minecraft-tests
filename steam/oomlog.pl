#!/usr/bin/perl -w
use strict;

my @alllines = <DATA>;
printf("Lines: %d\n", scalar(@alllines));

my ($aggrvm, $aggrrss, $steamvm) = (0,0,0);
foreach my $line (@alllines) {
    chomp($line);
    if ( $line =~ m/\[[\d\.]+\]\s+\[\s*(\w+|\d+)\s*\](.*)$/ ) {
        my ($pid, $res) = ($1, $2);
        if ( $res =~ m/^\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*([\-\d]+)\s*(\S+)\s*$/ ) {
            my ($uid,$tgid,$vm,$rss,$npte,$swap,$adj,$nm) = ($1,$2,$3,$4,$5,$6,$7,$8);
            printf("match  : %6s  %6d %6d  %s", $pid, $vm, $rss, $nm);
            $aggrvm += $vm; $aggrrss += $rss;
            if ( $nm =~ m/(steam|Steam|game)/ ) {
                print " *** ";
                $steamvm += $vm;
            }
            print "\n";
        } else {
            printf("match  : %6s  res %s\n", $pid, $res);
        }
    } elsif ( $line =~ m/^\s*$/ ) {
        ;#printf("nomatch: <empty line>\n");
    } elsif ( $line =~ m/\[[\d\.]+\]\s+(systemd\[\s*(\w+|\d+)\s*\])(.*)$/ ) {
        ;#printf("nomatch: systemd %s\n", $1);
    } else {
        printf("nomatch: %s\n", $line);
    }
}

printf("  total vm $aggrvm   total rss $aggrrss   total steam vm $steamvm\n");
#  total vm 2175649   total rss 348438   total steam vm 336470

exit 0

__END__

[42125.561240] [ pid ]   uid  tgid total_vm      rss nr_ptes swapents oom_score_adj name
[42125.561260] [   94]     0    94    17438      132      30        0             0 systemd-journal
[42125.561276] [  120]     0   120     3353       54       6        0             0 lvmetad
[42125.561290] [  127]     0   127     2616      174       6        0         -1000 systemd-udevd
[42125.561305] [  206]     0   206      925       49       9        0             0 alsactl
[42125.561320] [  214]     0   214     8405     2112      24        0             0 firewalld
[42125.561334] [  215]     0   215     9211      208      12        0             0 accounts-daemon
[42125.561349] [  216]   172   216     5313       50       7        0             0 rtkit-daemon
[42125.561363] [  218]     0   218   205952      413     247        0             0 rsyslogd
[42125.561378] [  230]    32   230     1256       84       5        0             0 rpcbind
[42125.561391] [  232]     0   232     1263      127       5        0             0 smartd
[42125.561405] [  233]     0   233     9731      218      18        0             0 ModemManager
[42125.561419] [  237]     0   237     1014       62       5        0             0 irqbalance
[42125.561433] [  238]     0   238     1013      109       4        0             0 systemd-logind
[42125.561447] [  239]    81   239     1198      288       5        0          -900 dbus-daemon
[42125.561461] [  244]   995   244      850       63       4        0             0 chronyd
[42125.561475] [  247]     0   247     1400       99       6        0             0 bluetoothd
[42125.561489] [  249]     0   249      591       22       6        0             0 mcelog
[42125.561502] [  251]     0   251     1588      158       5        0             0 crond
[42125.561515] [  254]     0   254      855       44       4        0             0 atd
[42125.561529] [  262]     0   262     8858      189      20        0             0 lightdm
[42125.561543] [  310]   999   310    18255     1178      20        0             0 polkitd
[42125.561556] [  359]     0   359    13802      387      18        0             0 NetworkManager
[42125.561571] [  403]   996   403     1380      148       5        0             0 systemd
[42125.561584] [  412]   996   412     1757      283       6        0             0 (sd-pam)
[42125.561598] [  498]     0   498     2756      150       9        0         -1000 sshd
[42125.561611] [  525]    29   525     1375      185       5        0             0 rpc.statd
[42125.561625] [  640]     0   640     5743      306      20        0             0 console-kit-dae
[42125.561640] [  709]  1006   709     1379      147       5        0             0 systemd
[42125.561653] [  714]  1006   714     1757      289       6        0             0 (sd-pam)
[42125.561667] [  771]     0   771    13103      365      12        0             0 udisksd
[42125.561680] [ 1340]     0  1340     1380      148       5        0             0 systemd
[42125.561694] [ 1351]     0  1351     1757      299       6        0             0 (sd-pam)
[42125.561708] [ 1510]     0  1510    11515      429      16        0             0 upowerd
[42125.561722] [ 2367]  1000  2367     1380      147       5        0             0 systemd
[42125.561735] [ 2375]  1000  2375     1855      307       6        0             0 (sd-pam)
[42125.561749] [ 2599]     0  2599    32284     9110      70        0             0 X
[42125.561762] [ 2614]   996  2614      932       75       4        0             0 dbus-launch
[42125.561776] [ 2615]   996  2615      988       63       4        0             0 dbus-daemon
[42125.561790] [ 2617]   996  2617     8889      101      17        0             0 at-spi-bus-laun
[42125.561804] [ 2620]   996  2620      988       56       5        0             0 dbus-daemon
[42125.561818] [ 2623]   996  2623     4491      151      16        0             0 at-spi2-registr
[42125.561832] [ 2633]     0  2633     4742      215      23        0             0 lightdm
[42125.561846] [ 2659]  1000  2659     1337       42       8        0             0 startkde
[42125.561859] [ 2666]  1000  2666      919       61       5        0             0 dbus-launch
[42125.561874] [ 2667]  1000  2667     1155      187       5        0             0 dbus-daemon
[42125.561888] [ 2674]  1000  2674     2010      110       6        0             0 ssh-agent
[42125.561902] [ 2713]  1000  2713     1376       71      11        0             0 gpg-agent
[42125.561915] [ 2728]  1000  2728      520       14       4        0             0 start_kdeinit
[42125.561930] [ 2729]  1000  2729    16784      394      42        0             0 kdeinit4
[42125.561943] [ 2730]  1000  2730    19501      372      50        0             0 klauncher
[42125.561957] [ 2732]  1000  2732    49776     1644      93        0             0 kded4
[42125.561970] [ 2734]  1000  2734      925       63       8        0             0 gam_server
[42125.561984] [ 2737]  1000  2737    23598      891      58        0             0 kglobalaccel
[42125.561998] [ 2747]  1000  2747      554       16       6        0             0 kwrapper4
[42125.562012] [ 2748]  1000  2748    41408     1022      87        0             0 ksmserver
[42125.562026] [ 2750]  1000  2750    37886      974      66        0             0 kactivitymanage
[42125.562040] [ 2757]  1000  2757   108817     6661     125        0             0 kwin
[42125.562054] [ 2771]  1000  2771   124300    21921     151        0             0 plasma-desktop
[42125.562068] [ 2785]  1000  2785    23402      704      57        0             0 kuiserver
[42125.562082] [ 2796]  1000  2796    19492      250      44        0             0 nepomukserver
[42125.562096] [ 2801]  1000  2801    65034     1899      92        0             0 krunner
[42125.562110] [ 2804]  1000  2804    25415      484      17        0             0 pulseaudio
[42125.562124] [ 2806]  1000  2806    27365     1396      62        0             0 nepomukstorage
[42125.562138] [ 2825]  1000  2825    26212      846      60        0             0 polkit-kde-auth
[42125.562152] [ 2826]  1000  2826    23492      747      57        0             0 klipper
[42125.562166] [ 2829]  1000  2829    27357      989      65        0             0 knotify4
[42125.562179] [ 2839]  1000  2839     3448      217      20        0             0 geoclue-master
[42125.562194] [ 2842]  1000  2842     7732      109      21        0             0 gvfsd
[42125.562207] [ 2848]  1000  2848    11562      132      20        0             0 gvfsd-fuse
[42125.562232] [ 2900]  1000  2900    13773     7500      39        0             0 virtuoso-t
[42125.562246] [ 2915]  1000  2915    29225     1042      65        0             0 nepomukfileinde
[42125.562260] [ 2917]  1000  2917    31744     1279      64        0             0 nepomukfilewatc
[42125.562275] [ 2941]     0  2941     2323      156       7        0             0 wpa_supplicant
[42125.562289] [ 2945]  1000  2945    23771      726      56        0             0 kwalletd
[42125.562302] [ 3092]  1000  3092    29441     2471      68        0             0 konsole
[42125.562316] [ 3094]  1000  3094     1526      250       8        0             0 bash
[42125.562330] [ 3156]  1000  3156     1526      233       8        0             0 bash
[42125.562343] [ 3185]  1000  3185     2714      148       8        0             0 shell
[42125.562356] [ 3198]  1006  3198     1515      218       8        0             0 bash
[42125.562369] [ 3616]  1006  3616     9714      220      12        0             0 schedlr
[42125.562383] [ 3695]  1006  3695      868       68       5        0             0 bash
[42125.562397] [ 3711]  1006  3711     1434      119       5        0             0 shell
[42125.562410] [ 3720]  1006  3720      894       69       6        0             0 bash
[42125.562423] [ 3736]  1006  3736      852       47       5        0             0 bash
[42125.562436] [ 3745]  1006  3745      887       76       6        0             0 bash
[42125.562450] [ 3746]  1006  3746      576       21       5        0             0 tee
[42125.562463] [ 3830]  1006  3830    54678    17220      98        0             0 steam
[42125.562476] [ 3832]  1006  3832    23628     4377      41        0             0 steam
[42125.562490] [ 3833]  1006  3833    65102     3065      73        0             0 steamwebhelper
[42125.562504] [ 3834]  1006  3834    28619      837      38        0             0 steamwebhelper
[42125.562519] [ 3835]  1006  3835    29615      839      38        0             0 steamwebhelper
[42125.562533] [ 3875]  1006  3875    52511     7010      97        0           300 steamwebhelper
[42125.562547] [ 4789]     0  4789     3641      341      10        0             0 sendmail
[42125.562561] [ 4815]    51  4815     3535      295      10        0             0 sendmail
[42125.562575] [ 4820]  1006  4820    54580    10952      89        0             0 SteamChildMonit
[42125.562590] [ 4821]  1006  4821   415018   215210     700        0             0 Civ5XP
[42125.562603] [ 4824]  1006  4824    27737     3486      43        0             0 gameoverlayui
[42125.562619] [ 5740]  1000  5740    89251     6765     104        0             0 kscreenlocker_g
[42125.562637] [ 5789]  1000  5789    10655      207      36        0             0 kcminit
[42125.562650] [ 5794]  1000  5794    10655      207      36        0             0 kcminit
[42125.562664] [ 5795]  1000  5795    23463      787      58        0             0 kcminit
[42125.562677] [ 5796]  1000  5796    23463      787      58        0             0 kcminit
[42125.562691] Out of memory: Kill process 4821 (Civ5XP) score 447 or sacrifice child
[42125.562705] Killed process 4821 (Civ5XP) total-vm:1660072kB, anon-rss:788136kB, file-rss:72704kB
[42136.283262] systemd[1]: Received SIGCHLD from PID 5789 (kcminit).
[42136.284407] systemd[1]: Child 5789 (kcminit) died (code=exited, status=0/SUCCESS)
[42136.285599] systemd[1]: Child 5794 (kcminit) died (code=exited, status=0/SUCCESS)
[42137.183222] systemd[1]: Received SIGCHLD from PID 5795 (kcminit).
[42137.183292] systemd[1]: Child 5795 (kcminit) died (code=exited, status=0/SUCCESS)
[42137.183493] systemd[1]: Received SIGCHLD from PID 5796 (kcminit).
[42137.183540] systemd[1]: Child 5796 (kcminit) died (code=exited, status=0/SUCCESS)
[42156.435637] systemd[1]: Got D-Bus request: org.freedesktop.DBus.NameOwnerChanged() on /org/freedesktop/DBus
[42156.485584] systemd[1]: Got D-Bus request: org.freedesktop.DBus.NameOwnerChanged() on /org/freedesktop/DBus
[42156.754320] systemd[1]: Got D-Bus request: org.freedesktop.systemd1.Activator.ActivationRequest() on /org/freedesktop/DBus
[42156.754353] systemd[1]: Got D-Bus activation request for fprintd.service
[42157.180658] systemd[1]: Trying to enqueue job fprintd.service/start/replace
[42157.181034] systemd[1]: Installed new job fprintd.service/start as 3886
[42157.181069] systemd[1]: Enqueued job fprintd.service/start as 3886
[42157.181144] systemd[1]: Starting Fingerprint Authentication Daemon...
[42157.181417] systemd[1]: About to execute: /usr/libexec/fprintd
[42157.181697] systemd[1]: Forked /usr/libexec/fprintd as 5829
[42157.186054] systemd[1]: fprintd.service changed dead -> start
[42157.186096] systemd[1]: Set up jobs progress timerfd.
[42157.186111] systemd[1]: Set up idle_pipe watch.
[42157.186161] systemd[5829]: Executing: /usr/libexec/fprintd
[42157.780450] systemd[1]: Got D-Bus request: org.freedesktop.DBus.NameOwnerChanged() on /org/freedesktop/DBus
[42157.782033] systemd[1]: Got D-Bus request: org.freedesktop.DBus.NameOwnerChanged() on /org/freedesktop/DBus
[42157.782069] systemd[1]: fprintd.service's D-Bus name net.reactivated.Fprint now registered by :1.174
[42157.782194] systemd[1]: fprintd.service changed start -> running
[42157.782214] systemd[1]: Job fprintd.service/start finished, result=done
[42157.782257] systemd[1]: Started Fingerprint Authentication Daemon.
[42157.782410] systemd[1]: Closed jobs progress timerfd.
[42157.782427] systemd[1]: Closed idle_pipe watch.
[42158.041920] systemd[1]: Got D-Bus request: org.freedesktop.DBus.NameOwnerChanged() on /org/freedesktop/DBus
[42158.673647] systemd[1]: Got D-Bus request: org.freedesktop.DBus.NameOwnerChanged() on /org/freedesktop/DBus
[42159.047778] systemd[1]: Got D-Bus request: org.freedesktop.DBus.NameOwnerChanged() on /org/freedesktop/DBus
[42188.047384] systemd[1]: Received SIGCHLD from PID 5829 (fprintd).
[42188.047450] systemd[1]: Child 5829 (fprintd) died (code=exited, status=0/SUCCESS)
[42188.047537] systemd[1]: Child 5829 belongs to fprintd.service
[42188.047571] systemd[1]: fprintd.service: main process exited, code=exited, status=0/SUCCESS
[42188.047824] systemd[1]: fprintd.service changed running -> dead
[42188.051628] systemd[1]: fprintd.service: cgroup is empty
[42188.051754] systemd[1]: Collecting fprintd.service
[42188.052097] systemd[1]: Got D-Bus request: org.freedesktop.DBus.NameOwnerChanged() on /org/freedesktop/DBus
[42188.052135] systemd[1]: Got D-Bus request: org.freedesktop.DBus.NameOwnerChanged() on /org/freedesktop/DBus
[42188.108611] systemd[1]: Accepted connection on private bus.
[42188.108877] systemd[1]: Got D-Bus request: org.freedesktop.systemd1.Agent.Released() on /org/freedesktop/systemd1/agent
[42188.109300] systemd[1]: Got D-Bus request: org.freedesktop.DBus.Local.Disconnected() on /org/freedesktop/DBus/Local
[42216.817369] systemd[1]: Received SIGCHLD from PID 3834 (steamwebhelper).
[42216.817440] systemd[1]: Child 3834 (steamwebhelper) died (code=exited, status=0/SUCCESS)
[42216.817558] systemd[1]: Child 3835 (steamwebhelper) died (code=exited, status=0/SUCCESS)

