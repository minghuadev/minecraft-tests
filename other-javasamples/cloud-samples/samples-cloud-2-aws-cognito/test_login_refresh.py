#!/usr/bin/env python
# test_login_refresn.txt

import requests
import json
import pprint

ENDPOINT_API = 'https://<id>.execute-api.<region>.amazonaws.com/<stage>/'


pp = pprint.PrettyPrinter(indent=4)

def login_login():
    print('\nREQUESTING login ++++++++++++++++++++++++++++++++++++')
    endpoint1 = ENDPOINT_API + 'user/login'

    req = { "username": "testusername", "password": "testpassword" }

    r = requests.post(endpoint1, data=json.dumps(req))
    print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
    print('Response code: %d\n' % r.status_code)
    pp.pprint( json.loads(r.text) )
    return json.loads(r.text)

def login_refresh(rtk):
    print('\nREQUESTING refresh ++++++++++++++++++++++++++++++++++++')
    endpoint2 = ENDPOINT_API + 'user/refreshtoken'

    req = {"username": "testusername", "refresh_token": rtk}

    r = requests.post(endpoint2, data=json.dumps(req))
    print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
    print('Response code: %d\n' % r.status_code)
    pp.pprint(json.loads(r.text))
    return json.loads(r.text)


r = login_login()
if r.get("success", False):
    d1 = r.get("data", None)
    d2 = d1.get("refresh_token", None)
    login_refresh(d2)

