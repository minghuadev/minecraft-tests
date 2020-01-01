#!/usr/bin/env python
# test1_4_2.txt
# https://stackoverflow.com/questions/51991401/how-to-implement-amazon-kinesis-putmedia-method-using-python


import requests
import sys
import os
import datetime
import hashlib
import hmac
import time
import pprint

pp = pprint.PrettyPrinter(indent=4)

# from test1_2
your_stream_name = 'my-video-stream-test'
def test1_2():
    import boto3

    client = boto3.client('kinesisvideo')
    response = client.get_data_endpoint(
        StreamName=your_stream_name,
        APIName='PUT_MEDIA'
    )
    pp.pprint(response)
    endpoint = response.get('DataEndpoint', None)
    print("endpoint %s" % endpoint)
    if endpoint is None:
        raise Exception("endpoint none")
    return endpoint


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def get_signature_key(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


# ************* REQUEST VALUES *************
method = 'POST'
service = 'kinesisvideo'
host = 'kinesisvideo.us-east-2.amazonaws.com'
region = 'us-east-2'
##endpoint = 'https://**<the endpoint you get with get_data_endpoint>**/PutMedia'
endpoint = test1_2()
# POST requests use a content type header. For DynamoDB,
# the content is JSON.
content_type = 'application/json'
start_tmstp = repr(time.time())

##localfile = 'test_1.png'
##localfile = '6-step_example.webm.360p.webm'
##localfile = 'big-buck-bunny_trailer.webm'
##localfile = 'test1.mkv'
##localfile = 'out.webm'
localfile = 'out28-6782.webm'

with open(localfile, 'rb') as image:
    request_parameters = image.read()

# Read AWS access key from env. variables or configuration file. Best practice is NOT
# to embed credentials in code.
access_key = '*************************'
secret_key = '*************************'
if access_key is None or secret_key is None:
    print('No access key is available.')
    sys.exit()

# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amz_date = t.strftime('%Y%m%dT%H%M%SZ')
date_stamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope

# ************* TASK 1: CREATE A CANONICAL REQUEST *************
# http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

# Step 1 is to define the verb (GET, POST, etc.)--already done.

# Step 2: Create canonical URI--the part of the URI from domain to query
# string (use '/' if no path)
canonical_uri = '/putMedia'

## Step 3: Create the canonical query string. In this example, request
# parameters are passed in the body of the request and the query string
# is blank.
canonical_querystring = ''

# Step 4: Create the canonical headers. Header names must be trimmed
# and lowercase, and sorted in code point order from low to high.
# Note that there is a trailing \n.
#'host:' + host + '\n' +
canonical_headers = 'x-amz-content-sha256:' + 'UNSIGNED-PAYLOAD' + '\n' + \
                    'x-amz-date:' + amz_date + '\n' + \
                    'x-amzn-fragment-timecode-type:' + 'RELATIVE' + '\n' + \
                    'x-amzn-producer-start-timestamp:' + start_tmstp + '\n' + \
                    'x-amzn-stream-name:' + your_stream_name + '\n'

# Step 5: Create the list of signed headers. This lists the headers
# in the canonical_headers list, delimited with ";" and in alpha order.
# Note: The request can include any headers; canonical_headers and
# signed_headers include those that you want to be included in the
# hash of the request. "Host" and "x-amz-date" are always required.
# For DynamoDB, content-type and x-amz-target are also required.
#
#in original sample  after x-amz-date :  + 'x-amz-target;'
signed_headers = 'x-amz-content-sha256;x-amz-date;' + \
                 'x-amzn-fragment-timecode-type;x-amzn-producer-start-timestamp;x-amzn-stream-name'

# Step 6: Create payload hash. In this example, the payload (body of
# the request) contains the request parameters.

# Step 7: Combine elements to create canonical request
canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers

# ************* TASK 2: CREATE THE STRING TO SIGN*************
# Match the algorithm to the hashing algorithm you use, either SHA-1 or
# SHA-256 (recommended)
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
string_to_sign = algorithm + '\n' + amz_date + '\n' + credential_scope + '\n' + hashlib.sha256(
    canonical_request.encode('utf-8')).hexdigest()

# ************* TASK 3: CALCULATE THE SIGNATURE *************
# Create the signing key using the function defined above.
signing_key = get_signature_key(secret_key, date_stamp, region, service)

# Sign the string_to_sign using the signing_key
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'),
                     hashlib.sha256).hexdigest()

# ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
# Put the signature information in a header named Authorization.
authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' + 'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

# # Python note: The 'host' header is added automatically by the Python 'requests' library.
headers = {
    'Content-Type': content_type,
    'x-amzn-fragment-timecode-type': 'ABSOLUTE',
    'x-amzn-producer-start-timestamp': start_tmstp,
    'x-amzn-stream-name': your_stream_name,
    # 'X-Amz-Target': amz_target,
    # 'x-amz-content-sha256': 'UNSIGNED-PAYLOAD',
    'Authorization': authorization_header
}

# ************* SEND THE REQUEST *************
print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
print('Request URL = ' + endpoint)

r = requests.post(endpoint, data=request_parameters, headers=headers)

print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)

