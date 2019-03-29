/*
 * urldownload.go
 */

package urldownload

import (
	"crypto"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/tls"
	"crypto/x509"
	"encoding/hex"
	"encoding/pem"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	"time"
)

func DownloadToFile(filepath string, url string) error {

	http.DefaultTransport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}

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

	http.DefaultTransport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}

	// Create the file
	//out, err := os.Create(filepath + ".part")
	out, err := os.Create(filepath)
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

	//err = os.Rename(filepath+".part", filepath)
	//if err != nil {
	//	fmt.Println("Failed rename")
	//	return err
	//}

	return nil
}

func VerifyArchiveSignature(pubkey string, filename string, sigfile string) bool {
	bytesPubkey, err := ioutil.ReadFile(pubkey)
	if err != nil {
		fmt.Println("Error: could not read pubkey file ", pubkey)
		fmt.Printf("Error: %v\n", err.Error())
		return false
	}
	block, _ := pem.Decode(bytesPubkey)

	pubBytes, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		fmt.Println("Error: failed to parse public key")
		fmt.Printf("Error: %v\n", err.Error()
		return false
	}

	file, err := os.Open(filename)
	if err != nil {
		fmt.Println("Error, failed to open archive\n")
		return false
	}
	defer file.Close()

	sha := sha256.New()
	if _, err = io.Copy(sha, file); err != nil {
		fmt.Println("Error: failed to take checksum")
		fmt.Printf("Error: %v\n", err.Error())
		return false
	}

	data, err := hex.DecodeString(sigfile)
	var byteSignature [256]byte
	if err != nil {
		fmt.Println("Error: could not parse signature")
		fmt.Printf("Error: %v\n", err.Error())
		return false
	}
	if len(data) < 256 {
		fmt.Println("Error: signature too short")
		return false
	}

	copy(byteSignature[0:256], data[0:256])

	err = rsa.VerifyPKCS1v15(pubBytes.(*rsa.PublicKey), crypto.SHA256, sha.Sum(nil), byteSignature[0:256])
	if err != nil {
		fmt.Println("Error: wrong signature")
		fmt.Printf("Error: %v\n", err.Error())
		return false
	}
	return true
}

