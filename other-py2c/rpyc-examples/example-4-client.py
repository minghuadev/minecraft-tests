#!/usr/bin/env python

# https://github.com/tomerfiliba-org/rpyc/issues/306

import rpyc
import time

np_client = rpyc.core.stream.NamedPipeStream.create_client("floop")
conn = rpyc.classic.connect_stream(np_client)

tm1 = time.time()

rmod = conn.modules.example_4_server_modules
print(" exampe-4-client: ", " rmod.names ", rmod.instance_one.get_names() )

tm2 = time.time()

conn.close()

print(" example-4-client: ", "time used %.3f" % (tm2 - tm1))

