// t2.go
package main

import "fmt"

func makeEvenGenerator() func() uint {
        i := uint(0)
        return func() (ret uint) {
                ret = i
                i += 2
                return
        }
}
func main2() {
        nextEven := makeEvenGenerator()
        fmt.Println(nextEven()) // 0
        fmt.Println(nextEven()) // 2
        fmt.Println(nextEven()) // 4
}

func main() {
        fmt.Println("hello world")
        var ta [14]int
        ta = [14]int{1, 2}
        fmt.Println(" ta ", ta)
        main2()
}
