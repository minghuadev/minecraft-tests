/*
 * packagecli.go
 */

package main

import (
	"fmt"
	"os"
	"path"
	"time"
)

/* download files:
               "<proj>/downloads/<filename>"
* src blob:
               "<proj>/src/<branch>/<filepath>"
* Here a proj is really a bitbucket repo name
*/

const info_list_team string = "your_team_name"
const info_list_proj string = "your_repo_name"

const info_package_team string = "your_team_name"
const info_package_proj string = "your_repo_name"

type RepoInfo_t struct {
	user string
	pass string
}

var repoinfo = RepoInfo_t{}

func GetRepoFileUrl(filename string) (fpth, furl string) {
	filepath := GetRepoDownloadPath(info_package_proj, filename)
	fileUrl := GetRepoApiUrl(repoinfo.user, repoinfo.pass, info_package_team, filepath)
	return filepath, fileUrl
}

func main() {

	var user, pass string
	var ok bool
	var pkg_list string = ""
	for {
		user, pass, ok = GetUserPass("envuserpass", 4)
		if !ok {
			fmt.Println("Failed to get a valid user-ID and password")
			os.Exit(1)
		}

		fmt.Println("")

		fmt.Println("Getting package list file")
		filepath := GetRepoRawPath(info_list_proj, "master", "package_list_rolling")
		filename := path.Base(filepath)

		fmt.Println("Download file : " + filepath + " to " + filename)

		fileUrl := GetRepoApiUrl(user, pass, info_list_team, filepath)
		err := DownloadToFileWithTee(filename, fileUrl)
		if err != nil {
			fmt.Println("Cannot get a valid package_list_rolling file. Check the network connection, " +
				"make sure the user-ID has the permission, and make sure the password is correct. ")
			// take out user:pass part from the error
			fmt.Println(BitBUrlRemoveUserPass(err.Error()))
			fmt.Println("Will retry in 10 seconds\n")
			time.Sleep(10 * 1000 * 1000 * 1000) // ns
		} else {
			pkg_list = filename
			repoinfo.user = user
			repoinfo.pass = pass
			break
		}
	}

	for {
		fmt.Println("")
		cmd := GetUser("Package command >> ")
		if len(cmd) > 2 {
			fmt.Printf("Run command \"%s\"\n", cmd)
			ok := PackageCommand(cmd, pkg_list)
			if ok {
				fmt.Printf("Ok finished command \"%s\"\n", cmd)
			} else {
				fmt.Printf("Failed command \"%s\"\n", cmd)
			}
		} else {
			PackageCommandHelp()
		}
	}
}
