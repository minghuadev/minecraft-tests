#!/bin/bash

rc=0

osname=$(uname -o)
if [ $osname == 'Cygwin' ]; then 
  getpass=getpass_dummy
else
  getpass=getpass
fi

echo  go build packagecli.go packagecmd.go packageinstall.go download.go bitbnames.go bitbids.go ${getpass}.go
ls -l packagecli
go       build packagecli.go packagecmd.go packageinstall.go download.go bitbnames.go bitbids.go ${getpass}.go
rc=$?
ls -l packagecli


if [ $rc -ne 0 ]; then
  echo; echo Failed compiling one or more targets. ; echo
else
  echo; echo OK compiling one or more targets. ; echo
fi
exit $rc

