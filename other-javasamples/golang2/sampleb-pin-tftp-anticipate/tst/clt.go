//
// clt.go
//    a client example for github.com/pin/tftp
//

package main

import (
	"github.com/pin/tftp"
	"time"
)
import (
	"fmt"
	"os"
)

func main() {

	tm0 := time.Now().UnixNano()

	ok := "failed" /* default fail */
	rxsize := int64(0)
	var rxerr error = nil
	for { /* scope */
		//c, err := tftp.NewClient("172.16.4.21:69")
		c, err_c := tftp.NewClient("127.0.0.1:69")
		if err_c != nil {
			rxerr = err_c
			break
		}

		/* local server. default: 7M. 512: 7M. 4096: 50M. 1440: 20M. total 51397632 bytes. */
		/* tftpd32. default: 7M. 1444: 19M. 4096: 40M.
		 *          size/anticipation     4096/4096: 60M. 4096/8192: 67M.
		 *                  512/511: 7M. 512/512: 14M. 512/1024..61440..65024: 15M.
		 *                  512/65536: 1.4M with 32 timeouts
		 *          total 51477700 bytes.
		 */
		//c.SetBlockSize(512)
		c.SetBlockSize(1440)

		wt, err_wt := c.Receive("foobar.bin", "octet")
		if err_wt != nil {
			rxerr = err_wt
			break
		}

		file, err_file := os.Create("rcvd.file")
		if err_file != nil {
			rxerr = err_file
			break
		}

		// Optionally obtain transfer size before actual data.
		if n, ok := wt.(tftp.IncomingTransfer).Size(); ok {
			fmt.Printf("Transfer size: %d\n", n)
		}
		n, err_wr := wt.WriteTo(file)
		fmt.Printf("%d bytes received\n", n)
		if err_wr != nil {
			rxerr = err_wr
			break
		}

		rxsize = n
		ok = "  ok  "
		break /* for scope */
	}

	tm1 := time.Now().UnixNano()
	var tdif int64 = (tm1 - tm0) / int64(time.Millisecond) /* msec */
	var spdk int64 = rxsize / tdif                         /* kBps */
	fmt.Printf("  rx %s  cost %v.%v speed %v.%v\n",
		ok, tdif/1000, tdif%1000, spdk/1000, spdk%1000)
	if rxerr != nil {
		fmt.Printf("      rxerr %v\n", rxerr)
	}
}
