/*
 * getpass.go
 */

package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"syscall"
)

/* https://stackoverflow.com/questions/2137357/getpasswd-functionality-in-go */

func GetPass(prompt string) string {
	fmt.Print(prompt)

	// Common settings and variables for both stty calls.
	attrs := syscall.ProcAttr{
		Dir:   "",
		Env:   []string{},
		Files: []uintptr{os.Stdin.Fd(), os.Stdout.Fd(), os.Stderr.Fd()},
		Sys:   nil}
	var ws syscall.WaitStatus

	// Disable echoing.
	pid, err := syscall.ForkExec(
		"/bin/stty",
		[]string{"stty", "-echo"},
		&attrs)
	if err != nil {
		panic(err)
	}

	// Wait for the stty process to complete.
	_, err = syscall.Wait4(pid, &ws, 0, nil)
	if err != nil {
		panic(err)
	}

	// Echo is disabled, now grab the data.
	reader := bufio.NewReader(os.Stdin)
	text, err := reader.ReadString('\n')
	if err != nil {
		panic(err)
	}

	// Re-enable echo.
	pid, err = syscall.ForkExec(
		"/bin/stty",
		[]string{"stty", "echo"},
		&attrs)
	if err != nil {
		panic(err)
	}

	// Wait for the stty process to complete.
	_, err = syscall.Wait4(pid, &ws, 0, nil)
	if err != nil {
		panic(err)
	}

	return strings.TrimSpace(text)
}

func GetUser(prompt string) string {
	fmt.Print(prompt)

	reader := bufio.NewReader(os.Stdin)
	text, err := reader.ReadString('\n')
	if err != nil {
		panic(err)
	}

	return strings.TrimSpace(text)
}

func GetUserPassEnv(envname string) (u string, p string, is_ok bool) {
	file, err := os.Open(envname)
	if err != nil {
		return "", "", false
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	userbytes, toolong1, err1 := reader.ReadLine()
	passbytes, toolong2, err2 := reader.ReadLine()

	var user, pass string
	var ok bool
	if !toolong1 && !toolong2 && err1 == nil && err2 == nil {
		user = string(userbytes)
		pass = string(passbytes)
		ok = true
	} else {
		user = ""
		pass = ""
		ok = false
	}
	return user, pass, ok
}
