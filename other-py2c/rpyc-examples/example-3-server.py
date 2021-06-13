#!/usr/bin/env python

# https://rpyc.readthedocs.io/en/latest/api/core_stream.html
# https://github.com/tomerfiliba-org/rpyc/issues/306
# pip install rpyc==5.0.1 plumbum==1.7.0 pypiwin32==223 pywin32==301 PySimpleGUI==4.43.0

import rpyc
from rpyc.core.stream import NamedPipeStream

def main():
    np_server = NamedPipeStream.create_server("floop")
    server = rpyc.classic.connect_stream(np_server)
    try:
        server.serve_all()
        print(" example-3-server: ", "serve_all() done")
    except:
        print(" example-3-server: ", "exception unknown")
    finally:
        server.close()

if __name__ == '__main__':
    main()

