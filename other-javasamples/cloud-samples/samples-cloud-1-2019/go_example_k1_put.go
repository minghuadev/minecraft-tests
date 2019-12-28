//
// src/sample_exercises/go_example_k1/go_example_k1_put.go
//

package main

import (
	"fmt"
	"math/rand"
	"os"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	kin "github.com/aws/aws-sdk-go/service/kinesis"
)

/* environment:
	 export AWS_ACCESS_KEY_ID=YOUR_AKID
	 export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
 * command argument:
	 the kinesis stream name
*/

type ReferrerData struct {
	EventTime string
	Tracker   string
}

func getReferrer() ReferrerData {
	data := ReferrerData{EventTime:"", Tracker:""}
	now := time.Now()
	str_now := now.Format(time.RFC3339Nano)
	data.EventTime = str_now
	choice := [5]string{"AAPL", "AMZN", "MSFT", "INTC", "TBV"}
	data.Tracker = choice[rand.Int31n(5)]
	return data
}

// Lists all objects in a bucket using pagination
//
// Usage:
// listObjects <bucket>
func main() {
	t0 := time.Now()

	if len(os.Args) < 2 {
		fmt.Println("you must specify a stream name")
		return
	}

	sess := session.Must(session.NewSession(&aws.Config{Region: aws.String("us-east-2")}))
	svc := kin.New(sess)

	for loopcnt:=0; loopcnt<4; loopcnt++ {
		data := fmt.Sprintf("%v %s", getReferrer(), time.Now().Sub(t0))
		fmt.Printf(" data: %v\n", data)
		out, err := svc.PutRecord(
			&kin.PutRecordInput{
				StreamName: &os.Args[1],
				Data: []byte(data),
				PartitionKey: aws.String("partKey")})
		if err != nil {
			fmt.Println("failed to put record", err)
			return
		}
		fmt.Println("loopcnt ", loopcnt)
		fmt.Printf(" record %T %v\n", out, out)
	}
}
