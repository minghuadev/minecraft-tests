#!/usr/bin/env python
#  test6_kinesis_data_create.py

# https://aws.amazon.com/blogs/big-data/snakes-in-the-stream-feeding-and-eating-amazon-kinesis-streams-with-python/
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html

import boto3
import pprint
import time

kinesis = boto3.client('kinesis',
                       region_name=None, api_version=None,
                       endpoint_url='http://localhost:4567', # default None
                       use_ssl=False, # default True,
                       verify=None, aws_access_key_id=None, aws_secret_access_key=None,
                       aws_session_token=None, config=None)

pp = pprint.PrettyPrinter(indent=4)

# create and check stream
ts_create_0 = time.time()
status_create_ok = False
try:
    kinesis.create_stream(StreamName='ExampleOutputStream', ShardCount=1) # no retv
    status_create_ok = True
except:
    pass
ts_create_1 = time.time()
print("create ok %s" % str(status_create_ok))

ts_create_2 = time.time()
status_ready_ok = False
status_check_cnt = 0
while status_create_ok:
    status_check_cnt += 1
    stream_desc = kinesis.describe_stream(
        StreamName='ExampleOutputStream',
        Limit=10,
        #ExclusiveStartShardId='string'
    )
    print('status')
    pp.pprint(stream_desc)
    rv_meta = stream_desc.get('ResponseMetadata', dict())
    rv_http_status = rv_meta.get('HTTPStatusCode', 0)
    if rv_http_status == 200:
        rv_desc = stream_desc.get('StreamDescription', dict())
        rv_status = rv_desc.get('StreamStatus', "")
        if rv_status == 'ACTIVE':
            status_ready_ok = True
    if status_ready_ok:
        break
    import time
    time.sleep(0.001)
ts_create_3 = time.time()
print("status_check_cnt %d time %.3f %.3f %.3f" % (status_check_cnt,
        (ts_create_1 - ts_create_0), (ts_create_3 - ts_create_2), (ts_create_3 - ts_create_0)))

# list streams
stream_list = kinesis.list_streams(
    Limit=10, #Limit (integer) -- The maximum number of streams to list.
    #ExclusiveStartStreamName (string) -- The name of the stream to start the list with.
)
print("streams")
pp.pprint(stream_list)

# list shard
shard_list = kinesis.list_shards(StreamName="ExampleOutputStream", MaxResults=4)
print("shards")
pp.pprint(shard_list)

