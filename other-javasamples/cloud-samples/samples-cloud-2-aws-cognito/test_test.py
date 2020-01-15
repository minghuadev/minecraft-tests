#!/usr/bin/env python
# test_test.txt

import requests
import json

endpoint = 'https://<id>.execute-api.<region>.amazonaws.com/<stage>/'


endpoint += 'user/test'

r = requests.post(endpoint,
                  data=json.dumps({"user_access_token":'abcd'}))
print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)

