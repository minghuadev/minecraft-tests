/*
 * t5.go
 */

package main

import (
	"fmt"
	"os"
)

func f1(i int) {
	fmt.Printf(" run f1  i %d \n ", i)
}
func f2(i int) {
	fmt.Printf(" run f2  i %d \n", i)
}

type funcs func(i int)

func main() {
	var cmds = map[int]funcs{1: f1, 2: f2}
	var i int = 1
	switch {
	case len(os.Args) == 1:
		i = 1
	case len(os.Args) == 2:
		i = 2
	default:
		i = 3
	}
	switch i {
	case 1:
		cmds[i](i)
	case 2:
		cmds[i](i)
	default:
		fmt.Println(" unknown case ")
	}
}
