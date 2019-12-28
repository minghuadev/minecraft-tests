#!/usr/bin/env python
#  test1_sample.py

import boto3


def test11():
    client = boto3.client('kinesisvideo')
    response = client.create_stream(
        DeviceName='camera3',
        StreamName='my-video-stream-test',
        #MediaType='h265',
        KmsKeyId='kms_key',
        DataRetentionInHours=123,
        Tags={
            'tag_abcd': '1234'
        }
    )

    print(response)
    #{u'StreamARN': u'arn:aws:kinesisvideo:us-east-1:342548:stream/my-video-stream-test3/15509335',
    # 'ResponseMetadata':
    # {'RetryAttempts': 0, 'HTTPStatusCode': 200,
    #  'RequestId': '27f71ca4-693b-43c9-8e71-ac0bccda1f07',
    #  'HTTPHeaders':
    #  {'x-amzn-requestid': '27f71ca4-693b-43c9-8e71-ac0bccda1f07', 'date': 'Sat, 30 Nov 2019 06:28:53 GMT',
    #   'content-length': '96', 'content-type': 'application/json'}}}

def test12():
    client = boto3.client('kinesisvideo')
    response = client.get_data_endpoint(
        StreamName='my-video-stream-test3',
        #StreamARN='string',
        #APIName='PUT_MEDIA' | 'GET_MEDIA' | 'LIST_FRAGMENTS' | 'GET_MEDIA_FOR_FRAGMENT_LIST' | 'GET_HLS_STREAMING_SESSION_URL' | 'GET_DASH_STREAMING_SESSION_URL'
        APIName='GET_MEDIA'
    )
    print(response)
    endpoint = response.get('DataEndpoint', None)
    print("endpoint %s" % endpoint)
    if endpoint is not None:
        client2 = boto3.client('kinesis-video-media')
        response = client2.get_media(
            StreamName='my-video-stream-test',
            #StreamARN='string',
            StartSelector={
                #'StartSelectorType': 'FRAGMENT_NUMBER' | 'SERVER_TIMESTAMP' | 'PRODUCER_TIMESTAMP' | 'NOW' | 'EARLIEST' | 'CONTINUATION_TOKEN',
                'StartSelectorType': 'EARLIEST',
                #'AfterFragmentNumber': 'string',
                #'StartTimestamp': datetime(2015, 1, 1),
                #'ContinuationToken': 'string'
            }
        )
        print(response)


test12()

