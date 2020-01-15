#!/usr/bin/env python
# testws1.py

# dependencies:
#
#  websocket-client python package
#
#    $ pip list
#    Package          Version
#    ---------------- -------
#    pip              18.1
#    setuptools       40.6.2
#    six              1.12.0
#    websocket-client 0.54.0
#    wheel            0.32.3

import socket
from websocket import create_connection
import time
import json
import pprint

BASE_URL = 'wss://<id>.execute-api.<region>.amazonaws.com/<stage>'


pp = pprint.PrettyPrinter(indent=4)

class StateMachineWs:
    def __init__(self, msg=""):
        self._baseurl = BASE_URL
        self._debug = True

        self._ws = None
        self._open_ok = False
        self._recv_failed = None
        self._send_failed = None
        self._recv_cnt = 0
        try:
            self._ws = create_connection(self._baseurl,
                                         header = {'user_access_token': 'abcd'},
                            sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),))
            self._open_ok = True
            self._recv_failed = False
            self._send_failed = False
        except Exception as e:
            print("WS Error create_connection exception %s" % str(e))
        except:
            print("WS Error create_connection unknown")

        if self._open_ok:
            print("WS Sending 'Hello, World'...  ts %.3f" % time.time())
            self._ws.send("WS Hello, World %s" % msg)
            print("WS Sent")

            print("WS Receiving...")
            result = self._ws.recv()
            self._ws.handshake_response
            print("WS Received '%s'" % str(result))

    def push(self, msg):
        ret_ok = False
        ret_v = None
        if self._open_ok and not self._recv_failed and not self._send_failed:
            try:
                result = self._ws.send(msg)
                ret_v = result
                ret_ok = True
            except Exception as e:  # likely closed
                self._recv_failed = True
                print("WS Receiving failed %s" % (str(e)))
        return ret_ok, ret_v

    def recv(self):
        ret_ok = False
        ret_v = None
        if self._open_ok and not self._recv_failed:
            try:
                #print("WS Receiving ...")
                result = self._ws.recv()
                self._recv_cnt += 1
                #print("WS Received %d : '%s'" % (self._recv_cnt, result))
                ret_ok = True
                ret_v = result
            except Exception as e:  # likely closed
                self._recv_failed = True
                print("WS Receiving failed %s" % (str(e)))
        return ret_ok, ret_v

    def close(self):
        if self._ws != None:
            try:
                self._ws.send_close()
                time.sleep(1)
                self._ws.close()
            except:
                pass
            finally:
                self._ws = None
                self._open_ok = False


class TestWs:

    def error(self, msg):
        raise Exception(msg)

    def __init__(self):
        self._debug = True
        self._do_ws = True

    def test_updating(self):

        if self._do_ws:
            try:
                machws = StateMachineWs()
            except:
                print("except StateMachineWs(). return.")
                return

        tmstart = time.time()
        backend_closed = False
        max_loops = 6 * 60 * 5 # sleep .2 sec, 5 loops per second
        for r in range(max_loops):
            tmnow = time.time()

            calc_do_ws = False
            if self._do_ws:
                # sometimes the first ws message will be lost. thus
                #   url get the first message always
                if r > 0:
                    calc_do_ws = True

            if calc_do_ws:
                machws.push("hello no %d" % r)
                ok, topcontstr = machws.recv()
                if not ok:
                    break
                topcont = json.loads(topcontstr)
                print("topcont len %d" % len(topcont))
                pp.pprint(topcont)

            time.sleep(0.2)

        if self._do_ws:
            machws.close()
        tmfinish = time.time()
        consumed_time = tmfinish - tmstart
        print("Consumed time %.3f" % consumed_time)


if __name__ == "__main__":
    consumes = []
    mainloopcnt = 0
    while True:
        mainloopcnt += 1
        print("\nTests mainloop %d start\n" % mainloopcnt)
        mach = TestWs()
        cost = mach.test_updating()
        print("\nTests mainloop %d done\n" % mainloopcnt)
        consumes.append(cost)

        time.sleep(0.2) # 200 ms

        if mainloopcnt > 4:
            break

    print("\n\nTests all done\n")
    pp.pprint(consumes)

