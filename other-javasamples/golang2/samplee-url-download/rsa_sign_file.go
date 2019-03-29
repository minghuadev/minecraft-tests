/*
 * rsa_sign_file.go
 */

package main

import (
        "fmt"
        "crypto/rsa"
        "encoding/pem"
        "crypto/x509"
        "io/ioutil"
        "crypto/sha256"
        "os"
        "log"
        "io"
        "crypto/rand"
        "crypto"
)

func main() {
        if len(os.Args) < 3 {
                log.Fatal("Error: need arguments <prv-key> <file-to-be-signed>\n")
        }

        prv_bytes, err := ioutil.ReadFile(os.Args[1])
        if err != nil {
		log.Fatal("Error: prv_bytes: %v\n", err.Error())
        }
        prv_block, _ := pem.Decode(prv_bytes)

        prv_key, err := x509.ParsePKCS1PrivateKey(prv_block.Bytes)
        if err != nil {
		log.Fatal("Error: prv_key: %v\n", err.Error())
        }

        file, err := os.Open(os.Args[2])
        if err != nil {
		log.Fatal("Error: file: %v\n", err.Error())
        }
        defer file.Close()

        sha_stream := sha256.New()
        if _, err := io.Copy(sha_stream, file); err != nil {
		log.Fatal("Error: copy sha_stream from file: %v\n", err.Error())
        }

        signature, err := rsa.SignPKCS1v15(rand.Reader, prv_key, crypto.SHA256, sha_stream.Sum(nil))
        if err != nil {
		log.Fatal("Error: signature: %v\n", err.Error())
        }

        fmt.Println("Signature:\n")
        fmt.Printf("%x\n", signature)
}


