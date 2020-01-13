#!/usr/bin/env python
# test_test.txt

import requests


endpoint = 'https://<id>.execute-api.<region>.amazonaws.com/<stage>/'

endpoint += 'user/test'

r = requests.post(endpoint)
print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)

