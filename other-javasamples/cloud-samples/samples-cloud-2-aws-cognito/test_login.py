#!/usr/bin/env python
# test_login.txt

import requests
import json


endpoint = 'https://<id>.execute-api.<region>.amazonaws.com/<stage>/'

endpoint += 'user/login'

req = { "username": "testusername", "password": "testpassword" }

r = requests.post(endpoint, data=json.dumps(req))
print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)

