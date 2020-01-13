#!/usr/bin/env python
# test_signup.txt

import requests
import json


endpoint = 'https://<id>.execute-api.<region>.amazonaws.com/<stage>/'

endpoint += 'user/signup'

req = {"username": "testusername", "password": "testpassword",
       "email":"user@example.com", "name":"testname"}

r = requests.post(endpoint, data=json.dumps(req))
print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)

