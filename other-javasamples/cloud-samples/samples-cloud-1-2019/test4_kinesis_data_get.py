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
                                          #ShardId='shardId-000000000000',
                                          ShardIteratorType='TRIM_HORIZON')["ShardIterator"]
    loopcnt = 0
    last_ago = 0.0
    max_dif = 0.0
    while loopcnt < 4000:
        out = kinesis.get_records(ShardIterator=shard_it, Limit=2)
        shard_it = out["NextShardIterator"]
        retv_ago = out['MillisBehindLatest']
        retv_ago_sec, retv_ago_ms = int(retv_ago/1000), int(retv_ago % 1000)
        dif_ago = last_ago - retv_ago
        if dif_ago > max_dif: max_dif = dif_ago
        print("\n%s%s%s" % ( "Out for %d.%03d ago" % (retv_ago_sec, retv_ago_ms),
                             " %.2f hours diff %.2f sec max %.2f" % (
                                 retv_ago_sec / 3600.0, dif_ago, max_dif ),
                             " loopcnt %d" % loopcnt ))
        last_ago = retv_ago
        #pp.pprint(out)
        if len(out['Records']) < 1 and retv_ago_sec == 0 and retv_ago_ms == 0:
            break
        for x in out['Records']:
            pp.pprint(x)
        loopcnt += 1





