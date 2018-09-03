/*
 * t6.go
 */

package main

import (
	"fmt"
	"os"
)

func f1(i int) int {
	fmt.Printf(" run f1  i %d \n ", i)
	return i + 1
}

func f2(i int) int {
	fmt.Printf(" run f2  i %d \n", i)
	return i + 2
}

func main() {
	var cmds = map[int]func(int) int{1: f1, 2: f2}
	var i int = 1
	switch {
	case len(os.Args) == 1:
		i = 1
	case len(os.Args) == 2:
		i = 2
	default:
		i = 3
	}
	if x, ok := cmds[i]; ok {
		x(i)
	} else {
		fmt.Println(" unknown case ")
	}
}
