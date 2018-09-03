/*
 * bitbnames.go
 */

package main

import (
	"bytes"
	"strings"
)

const BitBUrlProtocol string = "https://"
const BitBUrlStem string = "@api.bitbucket.org/2.0/repositories/"

func GetRepoDownloadPath(proj, file string) string {
	return proj + "/downloads/" + file

}

func GetRepoRawPath(proj, branch, file string) string {
	return proj + "/src/" + branch + "/" + file
}

func GetRepoApiUrl(user, pass, team, filepath string) string {
	var buffer bytes.Buffer

	buffer.WriteString(BitBUrlProtocol)
	buffer.WriteString(user)
	buffer.WriteString(":")
	buffer.WriteString(pass)
	buffer.WriteString(BitBUrlStem)
	buffer.WriteString(team)
	buffer.WriteString("/")
	buffer.WriteString(filepath)
	fileUrl := buffer.String()
	return fileUrl
}

func BitBUrlRemoveUserPass(in_url string) string {
	// take out user:pass part from the error
	idx1 := strings.Index(in_url, BitBUrlProtocol)
	len1 := len(BitBUrlProtocol)
	idx2 := strings.Index(in_url, BitBUrlStem)
	var out_str string = in_url
	if idx2 >= idx1+len1 && idx1 >= 0 {
		out_str = string(in_url[0:idx1+len1] + "..." + in_url[idx2+1:])
	}
	return out_str
}
