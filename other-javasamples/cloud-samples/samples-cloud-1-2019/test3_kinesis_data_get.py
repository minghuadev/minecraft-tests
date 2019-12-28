#!/usr/bin/env python
#  test3_kinesis_data_get.py

# https://aws.amazon.com/blogs/big-data/snakes-in-the-stream-feeding-and-eating-amazon-kinesis-streams-with-python/
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html

import boto3
import pprint

kinesis = boto3.client('kinesis')

pp = pprint.PrettyPrinter(indent=4)

shard_list = kinesis.list_shards(StreamName="ExampleInputStream", MaxResults=4)
print("shards")
pp.pprint(shard_list)

if len(shard_list['Shards']) == 1:
    shard_id = shard_list['Shards'][0]['ShardId']
    shard_it = kinesis.get_shard_iterator(StreamName="ExampleInputStream",
                                          ShardId= shard_id, #'shardId-000000000000',
                                          ShardIteratorType='TRIM_HORIZON')["ShardIterator"]
    while True:
        out = kinesis.get_records(ShardIterator=shard_it, Limit=2)
        shard_it = out["NextShardIterator"]
        retv_behind = out['MillisBehindLatest']
        print("\nOut for %d.%03d ago" % ( int(retv_behind/1000), int(retv_behind % 1000) ))
        #pp.pprint(out)
        if len(out['Records']) < 1 and int(retv_behind/1000) == 0: break
        for x in out['Records']:
            pp.pprint(x)





