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

def login_refresh_info(uname, id_tk, access_tk=None):
    print('\nREQUESTING refresh ++++++++++++++++++++++++++++++++++++')
    endpoint2 = ENDPOINT_API + 'user/refreshinfo'

    if access_tk is None:
        req = {"username": uname}
    else:
        req = {"access_token": access_tk}
    print(req)

    hdrs = {"token": id_tk}

    r = requests.post(endpoint2, data=json.dumps(req), headers=hdrs)
    print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
    print('Response code: %d\n' % r.status_code)
    pp.pprint(json.loads(r.text))
    return json.loads(r.text)


import sys
if len(sys.argv) > 1:
    r = login_login()
else:
    r = {"success": True}

if r.get("success", False):
    d1 = r.get("data", None)
    d2 = None
    d3 = None
    if d1 is not None:
        d2 = d1.get("id_token", None)
        d3 = d1.get("access_token", None) # comment this line out to use username
    if d2 is None and d3 is None:
        d2 = u'eyJraWQiOiJWZE05Z0rg'
        d3 = u'eyJraWQiOiJLbNTuDJjOUTzt-A'
    login_refresh_info("testusername", d2, d3)

