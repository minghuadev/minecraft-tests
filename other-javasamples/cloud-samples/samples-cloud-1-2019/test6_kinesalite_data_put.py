#!/usr/bin/env python
#  test6_kinesalite_data_put.py

# https://docs.aws.amazon.com/streams/latest/dev/get-started-exercise.html

import json
import boto3
import random
import datetime

kinesis = boto3.client('kinesis',
                       region_name=None, api_version=None,
                       endpoint_url='http://localhost:4567', # default None
                       use_ssl=False, # default True,
                       verify=None, aws_access_key_id=None, aws_secret_access_key=None,
                       aws_session_token=None, config=None)


def getReferrer(index):
    data = {}
    now = datetime.datetime.now()
    str_now = now.isoformat()
    data['EVENT_TIME'] = str_now
    data['TICKER'] = random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV'])
    price = random.random() * 100
    data['PRICE'] = round(price, 2)
    data['INDEX'] = index
    return data


index_count=0
index_max=30
while True:
    index_count += 1
    data = json.dumps(getReferrer(index_count))
    print(data)
    kinesis.put_record(
        StreamName="ExampleOutputStream",
        Data=data,
        PartitionKey="partitionkey")
    if index_count >= index_max:
        break


