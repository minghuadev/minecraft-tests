//
// src/sample_exercises/example_k1/example_k1_get.go
//

package main

import (
	"fmt"
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

// Lists all objects in a bucket using pagination
//
// Usage:
// listObjects <bucket>
func main() {
	if len(os.Args) < 2 {
		fmt.Println("you must specify a stream name")
		return
	}

	sess := session.Must(session.NewSession(&aws.Config{Region: aws.String("us-east-2")}))
	svc := kin.New(sess)

	arg_max_list := int64(4)
	shd, err := svc.ListShards(&kin.ListShardsInput{
		StreamName: &os.Args[1],
		MaxResults: &arg_max_list,
		ExclusiveStartShardId:nil,
		NextToken:nil,
		StreamCreationTimestamp:nil })
	if err != nil {
		fmt.Println("failed to list objects", err)
		return
	}
	fmt.Printf(" shd type %T\n", shd)
	if *shd.Shards[0].ShardId != string("shardId-000000000000") {
		fmt.Println("failed to get shard id")
		return
	}
	shard_id := *shd.Shards[0].ShardId

	shard_it_out, err := svc.GetShardIterator(&kin.GetShardIteratorInput{
		StreamName:        aws.String("ExampleInputStream"),
		ShardId:           &shard_id, /* #ShardId='shardId-000000000000', */
		ShardIteratorType: aws.String("TRIM_HORIZON"),
	})
	if err != nil {
		fmt.Println("failed to get shard iterator")
		return
	}
	shard_it := shard_it_out.ShardIterator
	shards_limit := int64(4)

	t0 := time.Now()
	for loopcnt:=0; loopcnt<4000; loopcnt++ {
		out, err := svc.GetRecords(&kin.GetRecordsInput{ShardIterator: shard_it, Limit: &shards_limit})
		if err != nil {
			fmt.Println("failed to get record")
			return
		}
		tx := time.Now().Sub(t0)
		fmt.Printf("loopcnt %v time %v", loopcnt, tx)
		if len(out.Records) > 0 {
			fmt.Printf(" record %T %v\n", out, out)
		} else {
			fmt.Printf(" record %T  MillisBehindLatest: %v\n", out, *out.MillisBehindLatest)
		}
		shard_it = out.NextShardIterator
		retv_ago := *out.MillisBehindLatest
		if len(out.Records) < 1 && retv_ago == 0 {
			fmt.Println("failed to get record for the past")
			break
		}
		for i,x := range out.Records {
			fmt.Printf(" record %v : %T %s\n", i, x.Data, string(x.Data))
		}
	}
}
