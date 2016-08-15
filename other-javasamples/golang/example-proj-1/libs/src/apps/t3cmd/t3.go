// t3.go
package main

import "fmt"

func f(n int) {
	for i := 0; i < 10; i++ {
		fmt.Println("n = ", n, "  i = ", i)
	}
}

func main() {
	go f(1)
	go f(2)
	var input string
	fmt.Scanln(&input)
}
