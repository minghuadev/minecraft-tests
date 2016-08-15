//tour-stringer.go

package main

import "fmt"

type Ip [4]uint8
type Host string
type IpAddr map[Host]Ip

func (ip *Ip) String() string {
	return fmt.Sprintf("%d.%d.%d.%d", ip[0], ip[1], ip[2], ip[3])
}

func main() {
	hosts := IpAddr{
		"bob": {1, 2, 3, 4},
		"cay": {5, 6, 7, 8},
	}
	for name, ip := range hosts {
		fmt.Printf("%v (%T) : %v (%T)\n", name, name, ip, ip)
	}
}
