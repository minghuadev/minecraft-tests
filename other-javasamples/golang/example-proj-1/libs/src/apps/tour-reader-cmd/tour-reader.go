//tour-reader.go

package main

import (
	"fmt"
	"golang.org/x/tour/reader"
	"io"
	"os"
	"strings"
	"time"
)

type MyReader struct{}

// TODO: Add a Read([]byte) (int, error) method to MyReader.
func (r MyReader) Read(b []byte) (int, error) {
	b[0] = 'A'
	return 1, nil
}

func main1() {
	reader.Validate(MyReader{})
}

// main2 rot13

type rot13Reader struct {
	r io.Reader
}

func (r *rot13Reader) Read(b []byte) (int, error) {
	fmt.Println("in   len cap ", len(b), cap(b))
	n, err := r.r.Read(b)
	if err != nil {
		fmt.Printf("read n err errtype %v %v %T\n", n, err, err)
		return 0, err
	}
	fmt.Println("read n ", n)
	for i, x := range b {
		if i >= n {
			fmt.Println("done n i x", n, i, x)
			break
		}
		switch {
		case x >= byte('A') && x <= byte('Z') && x >= byte('N'):
			x = x - 13
		case x >= byte('A') && x <= byte('Z'):
			x = x + 13
		case x >= byte('a') && x <= byte('z') && x >= byte('n'):
			x = x - 13
		case x >= byte('a') && x <= byte('z'):
			x = x + 13
		}
		//fmt.Printf(" conv  %3d %s  to  %3d %s \n", b[i], string(b[i]), x, string(x))
		b[i] = x
	}
	return n, nil
}

func main2() {
	s := strings.NewReader("Lbh penpxrq gur pbqr!")
	r := rot13Reader{s}
	io.Copy(os.Stdout, &r)
}

func main3() {

}

func main() {
	t := time.Now()
	s := t.Second() % 3
	switch s {
	case 0:
		main1()
	case 1:
		main2()
	case 3:
		main3()
	}
	fmt.Printf(" done selection main %d\n", s+1)
}
