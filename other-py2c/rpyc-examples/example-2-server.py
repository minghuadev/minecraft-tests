#!/usr/bin/env python

# https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html
# pip install rpyc==4.1.5 plumbum==1.6.9 PySimpleGUI==4.43.0

import rpyc
import time, random

class MyService(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass
        print(" example-2-server: on_connect ")

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass
        print(" example-2-server: on_disconnect ")

    def exposed_get_answer(self): # this is an exposed method
        len1 = int(time.time()) % 9 + 1
        data1 = [x for x in range(len1)]
        len2s = []
        for i in range(len1):
            len2 = random.randint(0,9999) % 9 + 1
            len2s.append(len2)
            data2 = bytearray([x for x in range(len2)])
            data1[i] = data2
        print(" example-2-server: len1 ", len1, "  len2s ", len2s)
        return data1

    exposed_the_real_answer_though = 43     # an exposed attribute

    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port=18861,)
                       #protocol_config={'allow_pickle': True})
    t.start()

