#!/usr/bin/env python
#  test6_kinesalite_data_list.py

# https://aws.amazon.com/blogs/big-data/snakes-in-the-stream-feeding-and-eating-amazon-kinesis-streams-with-python/
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html

import boto3
import pprint

kinesis = boto3.client('kinesis',
                       #region_name=None, api_version=None,
                       endpoint_url='http://localhost:4567', # default None
                       #use_ssl=False, # default True,
                       #verify=None, aws_access_key_id=None, aws_secret_access_key=None,
                       #aws_session_token=None, config=None
                       )

pp = pprint.PrettyPrinter(indent=4)

# create and check stream
status_create_ok = False
try:
    #kinesis.create_stream(StreamName='ExampleOutputStream', ShardCount=1) # no retv
    status_create_ok = True
except:
    pass
print("create ok %s" % str(status_create_ok))

#stream_desc = kinesis.describe_stream(
#    StreamName='ExampleInputStream',
#    Limit=10,
#    #ExclusiveStartShardId='string'
#)
print('status')
#pp.pprint(stream_desc)

# list streams
stream_list = kinesis.list_streams(
    Limit=10, #Limit (integer) -- The maximum number of streams to list.
    #ExclusiveStartStreamName (string) -- The name of the stream to start the list with.
)
print("streams")
pp.pprint(stream_list)

# list shard
stream_name = 'ExampleOutputStream'
shard_list = {'Shards': []}
if stream_name in stream_list['StreamNames']:
    shard_list = kinesis.list_shards(StreamName=stream_name, MaxResults=4)
print("shards")
pp.pprint(shard_list)

if len(shard_list['Shards']) == 1:
    shard_id = shard_list['Shards'][0]['ShardId']
    shard_it = kinesis.get_shard_iterator(StreamName=stream_name,
                                          ShardId= shard_id, #'shardId-000000000000',
                                          #ShardId='shardId-000000000000',
                                          ShardIteratorType='TRIM_HORIZON')["ShardIterator"]
    loopcnt = 0
    last_ago = 0.0
    max_dif = 0.0
    rec_sums = 0
    while loopcnt < 4000:
        out = kinesis.get_records(ShardIterator=shard_it, Limit=20)
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
        xlen = len(out['Records'])
        if xlen > 0:
            rec_sums += xlen
            print("  records xlen %d" % xlen)
            #continue
        for x in out['Records']:
            pp.pprint(x)
        loopcnt += 1

    print("  rec_sums %d" % rec_sums)
