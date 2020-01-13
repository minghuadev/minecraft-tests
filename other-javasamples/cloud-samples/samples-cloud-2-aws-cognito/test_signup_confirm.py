#!/usr/bin/env python
# test_signup_confirm.txt

import requests
import json


endpoint = 'https://<id>.execute-api.<region>.amazonaws.com/<stage>/'

endpoint += 'user/signupconfirm'

req = {"username": "testusername", "password": "testpassword",
       "code":"123456"}

r = requests.post(endpoint, data=json.dumps(req))
print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)

