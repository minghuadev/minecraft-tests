/*
 * bitsids.go
 */

package main

import (
	"fmt"
	"strings"
)

func GetUserPass(envname string, retries uint) (u, p string, ok_arg bool) {
	var user, pass string
	var ok bool
	var trycnt uint = 0
	for {
		trycnt++
		user, pass, ok = GetUserPassEnv(envname)
		if ok {
			fmt.Printf("Got your user-ID \"%s\" and password \"%s\" from the \"%s\" file\n",
				user, strings.Repeat(".", len(pass)), "envuserpass")
		} else {
			fmt.Println("Enter your bitbucket.org user-ID and password below.")
			user = GetUser("  Accound ID : ")
			pass = GetPass("  Password   : ")
			for i := 0; i < len(pass); i++ {
				fmt.Print(".")
			}
			ok = true
		}
		if strings.Contains(user, "@") || strings.Contains(user, ".com") {
			fmt.Println("A user-ID cannot be the email address. Try again.")
		} else if ok {
			break
		}
		if trycnt > retries {
			fmt.Println("Failed to get a valid user-ID")
			break
		}
	}
	return user, pass, ok
}
