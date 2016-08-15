// t1.go
package main

import "fmt"
import "mypkg"

func main() {
	fmt.Println("Hello, 世界")
	fmt.Println("my add2int: ", mypkg.Add2int(1, 5))
}
