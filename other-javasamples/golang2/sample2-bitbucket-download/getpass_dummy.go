/*
 * getpass_dummy.go
 */

package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func GetUser(prompt string) string {
	fmt.Print(prompt)

	reader := bufio.NewReader(os.Stdin)
	text, err := reader.ReadString('\n')
	if err != nil {
		panic(err)
	}

	return strings.TrimSpace(text)
}

func GetPass(prompt string) string {
	return GetUser(prompt)
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
