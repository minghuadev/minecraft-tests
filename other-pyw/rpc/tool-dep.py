#!/usr/bin/env python3
# tool-dep.py
#
# ref: stackoverflow questions/41816693
#      how-to-list-dependencies-for-a-python-library-without-installing

import requests


def find_dep(n, v=None):
    if v is None:
        url = 'https://pypi.org/pypi/%s/json' % n
    else:
        url = 'https://pypi.org/pypi/%s/%s/json' % ( n, v )

    resp = requests.get(url)
    print("package: ", n, "" if n is None else v )
    print("resp: ", repr(resp))
    json = resp.json()
    #print("json: ", repr(json))
    required_pkgs = json['info']['requires_dist']
    print("deps: ", repr(required_pkgs))


pkgn="rpyc"
pkgv="4.1.5"
find_dep(pkgn, pkgv)

pkgn="plumbum"
pkgv="1.6.9"
find_dep(pkgn, pkgv)


# result: 
# package:  rpyc 4.1.5
# resp:  <Response [200]>
# deps:  ['plumbum']
# package:  plumbum 1.6.9
# resp:  <Response [200]>
# deps:  None


