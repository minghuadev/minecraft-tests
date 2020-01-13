#!/usr/bin/env python
# test_login_info.txt

import requests
import json
import pprint

ENDPOINT_API = 'https://<id>.execute-api.<region>.amazonaws.com/<stage>/'
USERNAME = "testusername"
PASSWORD = "testpassword"


pp = pprint.PrettyPrinter(indent=4)

def login_login():
    print('\nREQUESTING login ++++++++++++++++++++++++++++++++++++')
    endpoint1 = ENDPOINT_API + 'user/login'

    req = { "username": USERNAME, "password": PASSWORD }

    r = requests.post(endpoint1, data=json.dumps(req))
    print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
    print('Response code: %d\n' % r.status_code)
    pp.pprint( json.loads(r.text) )
    return json.loads(r.text)

def login_refresh_info(uname, atk):
    print('\nREQUESTING refresh ++++++++++++++++++++++++++++++++++++')
    endpoint2 = ENDPOINT_API + 'user/refreshinfo'

    req = {"username": uname}
    hdrs = {"token": atk}

    r = requests.post(endpoint2, data=json.dumps(req), headers=hdrs)
    print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
    print('Response code: %d\n' % r.status_code)
    pp.pprint(json.loads(r.text))
    return json.loads(r.text)


r = login_login()
if r.get("success", False):
    d1 = r.get("data", None)
    d2 = d1.get("id_token", None)
    login_refresh_info("testusername", d2)

