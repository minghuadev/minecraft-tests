//
// src/sample_exercises/go_example_s3/go_example_s3.go
//

package main

import (
	"fmt"
	"os"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
)

/* environment:
	 export AWS_ACCESS_KEY_ID=YOUR_AKID
	 export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
 * command argument:
	 the s3 bucket name
*/

// Lists all objects in a bucket using pagination
//
// Usage:
// listObjects <bucket>
func main() {
	if len(os.Args) < 2 {
		fmt.Println("you must specify a bucket")
		return
	}

	sess := session.Must(session.NewSession(&aws.Config{Region: aws.String("us-east-2")}))

	svc := s3.New(sess)

	i := 0
	err := svc.ListObjectsPages(&s3.ListObjectsInput{
		Bucket: &os.Args[1],
	}, func(p *s3.ListObjectsOutput, last bool) (shouldContinue bool) {
		fmt.Println("Page,", i)
		i++

		for _, obj := range p.Contents {
			fmt.Println("Object:", *obj.Key)
		}
		return true
	})
	if err != nil {
		fmt.Println("failed to list objects", err)
		return
	}
}
