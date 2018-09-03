/*
 * download.go
 */

package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"
)

/* https://golangcode.com/download-a-file-from-a-url/ */
func DownloadToFile(filepath string, url string) error {

	// Create the file
	out, err := os.Create(filepath)
	if err != nil {
		fmt.Println("Failed os create %s", filepath)
		return err
	}
	defer out.Close()

	// Get the data
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("Failed http get url")
		return err
	}
	defer resp.Body.Close()

	// Write the body to file
	_, err = io.Copy(out, resp.Body)
	if err != nil {
		fmt.Println("Failed io copy resp to file")
		return err
	}

	return nil
}


/* https://golangcode.com/download-a-file-with-progress/ */

// write cycle.
type WriteCounter struct {
	LastTime time.Time
	LastLen  uint32
	Chunk    uint32
	Total    uint64
}

func (wc *WriteCounter) Write(p []byte) (int, error) {
	n := len(p)
	wc.Total += uint64(n)
	wc.Chunk += 1
	tmnow := time.Now()
	tmdif := tmnow.Sub(wc.LastTime).Seconds()
	// first tmdif  sec 9,223,372,036.85
	if tmdif > 2 || wc.Chunk == 1 {
		wc.LastLen = wc.PrintProgress(tmdif, wc.LastLen)
		wc.LastTime = tmnow
		if wc.LastLen > 250 {
			wc.LastLen = 250
		}
	}
	return n, nil
}

func (wc WriteCounter) PrintProgress(tmdif float64, minlen uint32) uint32 {
	//fmt.Printf("\r%s", strings.Repeat(" ", 35))
	str := fmt.Sprintf("Downloading... chunk %v, bytes completed %v, since last chunk %.2f ",
		wc.Chunk, wc.Total, tmdif)
	lenrec := len(str)
	var extralen uint32 = 1
	if lenrec > 0 && minlen > uint32(lenrec) {
		extralen = minlen - uint32(lenrec)
	}
	fmt.Printf("\r%s %s", str, strings.Repeat(" ", int(extralen)))
	var lenret uint32 = 0
	if lenrec > 0 {
		lenret = uint32(lenrec)
	}
	return lenret
}

func DownloadToFileWithTee(filepath string, url string) error {

	// Create the file
	out, err := os.Create(filepath + ".part")
	if err != nil {
		fmt.Println("Failed os create")
		return err
	}
	defer out.Close()

	// Get the data
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("Failed http get url")
		return err
	}
	defer resp.Body.Close()

	// Write the body to file
	counter := &WriteCounter{}
	counter.LastTime = time.Now()
	_, err = io.Copy(out, io.TeeReader(resp.Body, counter))
	if err != nil {
		fmt.Println("Failed io copy")
		return err
	}

	// The progress used the same same line
	fmt.Print("\n")

	err = os.Rename(filepath+".part", filepath)
	if err != nil {
		fmt.Println("Failed rename")
		return err
	}

	return nil
}
