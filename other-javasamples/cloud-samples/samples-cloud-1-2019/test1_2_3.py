#!/usr/bin/env python
#  test1_2.py

import boto3
import pprint
import time
import datetime

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

    last_timestamp = None
    seg_count = 20
    while True: # scope
        if endpoint is None:
            break # fail

        client2 = boto3.client('kinesis-video-media', endpoint_url=endpoint)
        if last_timestamp is None:
            response = client2.get_media(
                StreamName=your_stream_name,
                StartSelector={
                    'StartSelectorType': 'EARLIEST',
                }
            )
        else:
            # if updated last_timestamp, will continue from now
            startstamp = last_timestamp + 8 * 3600 # 8 * 3600 for -8 tz
            response = client2.get_media(
                StreamName=your_stream_name,
                StartSelector={
                    'StartSelectorType': 'SERVER_TIMESTAMP',
                    'StartTimestamp': datetime.datetime.fromtimestamp(startstamp),
                }
            )
            pass
        pp.pprint(response)
        stream = response['Payload'] # botocore.response.StreamingBody object

        seg_count += 1
        seg_any_data, seg_idle_count, seg_tm0, seg_frag = False, 0, time.time(), 0
        with open("out%02d.webm" % seg_count, "wb") as outf:
            while True:
                ret_ok, ret_sz = False, 0
                try:
                    frame = stream.read(640000)
                    if type(frame) is str:
                        print(" stream type frame %s len %-6d  seg_count %d frag %d" % (
                            type(frame), len(frame), seg_count, seg_frag))
                        ret_ok, ret_sz, seg_any_data = True, len(frame), True
                        outf.write(frame)
                        outf.flush()
                        seg_frag += 1
                        # if updated last_timestamp, will continue from now
                        # comment out to repeat get same data
                        last_timestamp = time.time()
                    else:
                        print(" stream type frame %s" % (type(frame)))
                except BaseException as e:
                    print("Exception")
                    print(e)
                except:
                    print("Exception unknown")
                if not ret_ok or ret_sz == 0:
                    seg_idle_count += 1
                    if seg_idle_count > 4:
                        print("Seg done at frag %d cost %.2f" % ( seg_frag, time.time() - seg_tm0))
                        break
                    print("Sleep 1.0")
                    time.sleep(1.0)
                else:
                    seg_idle_count = 0
            outf.close()
        if seg_any_data:
            continue
        break # scope

test1_2()

