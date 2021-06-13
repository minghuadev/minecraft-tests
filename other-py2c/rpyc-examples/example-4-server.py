#!/usr/bin/env python

# https://rpyc.readthedocs.io/en/latest/api/core_stream.html
# https://github.com/tomerfiliba-org/rpyc/issues/306
# pip install rpyc==5.0.1 plumbum==1.7.0 pypiwin32==223 pywin32==301 PySimpleGUI==4.43.0

import rpyc
from rpyc.core.stream import NamedPipeStream
import example_4_server_modules

def main_one(server_count):
    print(" example-4-server: ", " creating server count ", server_count)
    example_4_server_modules.instance_one.append_instance("server-count-%d" % server_count)
    np_server = NamedPipeStream.create_server("floop")
    server = rpyc.classic.connect_stream(np_server)
    print(" example-4-server: ", " connected server count ", server_count)
    try:
        server.serve_all()
        print(" example-4-server: ", "serve_all() done")
    except:
        print(" example-4-server: ", "exception unknown")
    finally:
        server.close()
    print(" example-4-server: ", " finishing server count ", server_count)

def main_main():
    server_count = 0
    while True:
        server_count += 1
        main_one(server_count)

if __name__ == '__main__':
    main_main()

