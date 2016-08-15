//tour-slice.go

package main

import "fmt"
import "golang.org/x/tour/pic"

func Pic(dx, dy int) [][]uint8 {
	x := make([][]uint8, 0, dy)
	for n := 0; n < dy; n++ {
		y := make([]uint8, 0, dx)
		for m := 0; m < dx; m++ {
			y = append(y, uint8((n+1)*(m+1)))
		}
		x = append(x, y)
	}
	return x
}

func main() {
	var p = Pic(3, 3)
	fmt.Println(p)
	pic.Show(Pic)
}
