/*
 * packageinstall.go
 */

package main

import (
	"fmt"
	"os"
	"os/exec"
	"time"
)

const sh_inst_cmd_sh string = `#!/bin/sh
#  sh-packageinst.sh

tmpdir=$1
arcfile=$2

if [ -z "$tmpdir" -o -z "$arcfile" ]; then
    echo Empty tmpdir $tmpdir or arcfile $arcfile
    exit 1
fi

echo Ok tmpdir $tmpdir arcfile $arcfile

set -e

echo cd $tmpdir
cd $tmpdir

echo pwd
pwd

echo tar zxfv ../$arcfile
tar zxfv ../$arcfile

echo pwd
pwd

echo ls
ls

echo sh control/install.sh
sh control/install.sh

`

func InstallPackage(fn0 string) bool {
	var ok bool = true

	script, err := os.Create("sh-packageinst.sh")
	if err != nil {
		fmt.Println("Failed open sh-packageinst.sh")
		return false // fail
	}
	fmt.Fprintf(script, "%s", sh_inst_cmd_sh)
	tmnow := time.Now()
	fmt.Fprintf(script, "\n# created at %d-%v-%d %d:%d:%d\n\n",
		tmnow.Year(), tmnow.Month(), tmnow.Day(), tmnow.Hour(), tmnow.Minute(), tmnow.Second())
	script.Close()

	instcmd := "./sh-packageinst.sh temppkg " + fn0
	cmds := []string{"pwd", "chmod +x sh-packageinst.sh", "ls -l sh-packageinst.sh",
		"rm -rf temppkg", "mkdir temppkg", instcmd}
	for i, cmd := range cmds {
		out, err := exec.Command("sh", "-c", cmd).Output()
		okval := " ok "
		if err != nil {
			ok = false
			okval = "fail"
		}
		fmt.Printf(" i %d  %s  cmd %s  output %s \n", i, okval, cmd, string(out))
		if !ok {
			break
		}
	}
	return ok
}
