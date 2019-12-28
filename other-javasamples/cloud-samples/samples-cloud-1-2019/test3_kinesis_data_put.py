#!/usr/bin/env python
#  test3_kinesis_data_put.py

# https://docs.aws.amazon.com/streams/latest/dev/get-started-exercise.html

import json
import boto3
import random
import datetime

kinesis = boto3.client('kinesis')


def getReferrer():
    data = {}
    now = datetime.datetime.now()
    str_now = now.isoformat()
    data['EVENT_TIME'] = str_now
    data['TICKER'] = random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV'])
    price = random.random() * 100
    data['PRICE'] = round(price, 2)
    return data


while True:
    data = json.dumps(getReferrer())
    print(data)
    kinesis.put_record(
        StreamName="ExampleInputStream",
        Data=data,
        PartitionKey="partitionkey")


