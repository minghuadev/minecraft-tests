#!/usr/bin/env python

# https://github.com/tomerfiliba-org/rpyc/issues/306

import rpyc
import time

np_client = rpyc.core.stream.NamedPipeStream.create_client("floop")
conn = rpyc.classic.connect_stream(np_client)

tm1 = time.time()
for i in range(1000):
    conn.ping()
tm2 = time.time()

conn.close()

print(" example-3-client: ", "time used %.3f" % (tm2 - tm1))

