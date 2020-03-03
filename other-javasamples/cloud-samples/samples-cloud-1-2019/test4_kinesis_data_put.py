#!/usr/bin/env python
#  test4_kinesis_data_put.py

# https://docs.aws.amazon.com/streams/latest/dev/get-started-exercise.html

import json
import boto3
import random
import datetime

import time
import pprint

kinesis = boto3.client('kinesis')

pp = pprint.PrettyPrinter(indent=4)

def getReferrer():
    data = {}
    now = datetime.datetime.now()
    str_now = now.isoformat()
    data['EVENT_TIME'] = str_now
    data['TICKER'] = random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV'])
    price = random.random() * 100
    data['PRICE'] = round(price, 2)
    return data

x = int(time.time())
for i in range(2):
    y = time.time()
    while y < x + 1:
        time.sleep(0.01)
        y = time.time()
    x = y
    data = json.dumps(getReferrer())
    print(data)
    rv = kinesis.put_record(
        StreamName="ExampleOutputStream",
        Data=data,
        PartitionKey="partitionkey")
    print(" rv type %s" % str(type(rv)))
    pp.pprint(rv)


