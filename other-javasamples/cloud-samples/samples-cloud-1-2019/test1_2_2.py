#!/usr/bin/env python
#  test1_2.py

import boto3
import pprint
import time

pp = pprint.PrettyPrinter(indent=4)

your_stream_name = 'my-video-stream-test'

def test1_2():
    client = boto3.client('kinesisvideo')
    response = client.get_data_endpoint(
        StreamName=your_stream_name,
        APIName='GET_MEDIA'
    )
    pp.pprint(response)
    endpoint = response.get('DataEndpoint', None)
    print("endpoint %s" % endpoint)
    if endpoint is not None:
        client2 = boto3.client('kinesis-video-media', endpoint_url=endpoint)
        response = client2.get_media(
            StreamName=your_stream_name,
            StartSelector={
                'StartSelectorType': 'EARLIEST',
            }
        )
        pp.pprint(response)
        stream = response['Payload'] # botocore.response.StreamingBody object

        with open("out.webm", "wb") as outf:
            while True:
                ret_ok = False
                ret_sz = 0
                try:
                    frame = stream.read(640000)
                    if type(frame) is str:
                        print(" stream type ret %d frame %s" % (len(frame), type(frame)))
                        ret_ok = True
                        ret_sz = len(frame)
                        outf.write(frame)
                        outf.flush()
                    else:
                        print(" stream type frame %s" % (type(frame)))
                except BaseException as e:
                    print("Exception")
                    print(e)
                except:
                    print("Exception unknown")
                if not ret_ok or ret_sz == 0:
                    print("Sleep 1.0")
                    time.sleep(1.0)

test1_2()

