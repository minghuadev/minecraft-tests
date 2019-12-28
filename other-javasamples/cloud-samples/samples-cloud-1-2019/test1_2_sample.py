#!/usr/bin/env python
#  test1_2_sample.py

import boto3
import pprint
import time

pp = pprint.PrettyPrinter(indent=4)


def test1_2():
    client = boto3.client('kinesisvideo')
    response = client.get_data_endpoint(
        StreamName='my-video-stream-test',
        APIName='GET_MEDIA'
    )
    pp.pprint(response)
    endpoint = response.get('DataEndpoint', None)
    print("endpoint %s" % endpoint)
    if endpoint is not None:
        client2 = boto3.client('kinesis-video-media', endpoint_url=endpoint)
        response = client2.get_media(
            StreamName='my-video-stream-test',
            StartSelector={
                'StartSelectorType': 'EARLIEST',
            }
        )
        pp.pprint(response)
        stream = response['Payload'] # botocore.response.StreamingBody object

        while True:
            ret_ok = False
            try:
                ret, frame = stream.read()
                print(" stream type ret %s frame %s" % (type(ret), type(frame)))
                ret_ok = True
            except BaseException as e:
                print("Exception")
                print(e)
            except:
                print("Exception unknown")
            if not ret_ok:
                time.sleep(1.0)


test1_2()

