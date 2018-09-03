/*
 * packagecmd.go
 */

package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// ----------------------------------------------------------------------

type package_element_t struct {
	pkgname     string
	buildno     uint
	filename    string
	size        int
	description string
}
type packages_t []package_element_t

var packages_table packages_t

// ----------------------------------------------------------------------

func exitquit_command(in_arg []string) bool {
	for i, s := range in_arg {
		fmt.Printf(" i %d s %s\n", i, s)
	}
	os.Exit(0)
	return false
}

func list_command(in_arg []string) bool {
	fmt.Println("List packages: name, buildno description")
	for i, x := range packages_table {
		fmt.Printf(" i %d  %s  %d  %d %s\n",
			i, x.pkgname, x.buildno, x.size, x.description)
	}
	return true
}

func install_command(in_arg []string) bool {
	fmt.Println("Install package: ")
	arglen := len(in_arg)
	if arglen < 2 {
		fmt.Println("  command args need to be 2 or more ")
		return false
	}
	var bn0 uint = 0
	var fn0 string = ""
	var foundpkg bool = false
	for _, x := range packages_table {
		if strings.Compare(in_arg[1], x.pkgname) == 0 && bn0 < x.buildno {
			bn0 = x.buildno
			fn0 = x.filename
			foundpkg = true
		}
	}
	if !foundpkg {
		fmt.Println("Failed to find the package")
		return false
	}
	fpth0, furl0 := GetRepoFileUrl(fn0)
	fmt.Println("Download file : " + fpth0 + " to " + fn0 + fmt.Sprintf(
		" build-no %v", bn0))
	err := DownloadToFileWithTee(fn0, furl0)
	if err != nil {
		fmt.Println("Failed download file")
		// take out user:pass part from the error
		fmt.Println(BitBUrlRemoveUserPass(err.Error()))
		return false
	}
	ok := InstallPackage(fn0)
	if !ok {
		fmt.Println("Failed install package")
		return false
	}
	return true
}

// ----------------------------------------------------------------------

type command_define_t struct {
	cmdfunct func([]string) bool
	usage    string
}
type commands_t map[string]command_define_t

var commands_table commands_t = map[string]command_define_t{
	"exit":    command_define_t{exitquit_command, " "},
	"quit":    command_define_t{exitquit_command, " "},
	"list":    command_define_t{list_command, " "},
	"install": command_define_t{install_command, " <pkg-name> [<build-no>]"},
}

// ----------------------------------------------------------------------

func PackageCommand(cmd_in, pkg_list string) bool {
	var ok bool = false
	for {
		if !create_package_table(pkg_list) {
			fmt.Println("Failed create package table")
			break
		}
		cmdargs := strings.Split(cmd_in, " ")
		var cmdline command_define_t
		var cmdok bool
		if cmdline, cmdok = commands_table[cmdargs[0]]; !cmdok {
			fmt.Println("Failed to resolve cmd function from table")
			PackageCommandHelp()
			break
		}
		cmdok = cmdline.cmdfunct(cmdargs[:])
		if !cmdok {
			break
		}
		ok = true
		break
	}
	return ok
}

func PackageCommandHelp() {
	fmt.Println("  No command or unknown command. Try: ")
}

// ----------------------------------------------------------------------

func create_package_table(pkg_list string) bool {
	packages_table = make(packages_t, 0)
	file, err := os.Open(pkg_list)
	if err != nil {
		return false
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	for {
		userbytes, toolong1, err1 := reader.ReadLine()
		if err1 != nil || toolong1 {
			break
		}
		theline := string(userbytes)
		elems := strings.Split(theline, "|")
		linehead := strings.TrimSpace(elems[0])
		if len(linehead) < 1 || strings.Index(linehead, "#") == 0 {
			continue
		}
		var n = package_element_t{}
		n.pkgname = linehead
		nlen := len(elems)
		if nlen >= 2 {
			nn, _ := strconv.ParseUint(strings.TrimSpace(elems[1]), 10, 32)
			n.buildno = uint(nn)
		}
		if nlen >= 3 {
			n.filename = strings.TrimSpace(elems[2])
		}
		if nlen >= 5 { // size was added late. if two more elements ...
			nn, _ := strconv.ParseUint(strings.TrimSpace(elems[3]), 10, 32)
			n.size = int(nn)
		}
		// description is always the last element
		if nlen >= 4 {
			n.description = strings.TrimSpace(elems[nlen-1])
		}
		packages_table = append(packages_table, n)
	}
	return true
}

// ----------------------------------------------------------------------
