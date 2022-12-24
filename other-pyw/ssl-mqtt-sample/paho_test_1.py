#!/usr/bin/env python
# paho_test_1.py
# 2022-12-24

# reference:
#   stackoverflow python-eclipse-paho-client-tls-connection-to-mqtt-broker-exception-no-ciphers
#   http://www.steves-internet-guide.com/into-mqtt-python-client/
# other reference: mosquitto tls
#   https://openest.io/en/services/mqtts-how-to-use-mqtt-with-tls/

# tested on windows10 paho.mqtt 1.6.1 with python 3.8.10


import ssl
import hashlib
import time

import paho.mqtt.client as paho


# Set device information here
HOSTNAME="mqtts.example.com"
PORT=8883
ca_cert = "broker-or-ca_certificate.pem"


# Locations of CA Authority, client certificate and client key file
#ca_cert = "ca_certificate.pem"
#client_cert = "client_certificate.pem"
#client_key = "client_key.pem"

PASS_WORD=hashlib.sha256( (USER_SALT + USER_PASS_CODE).encode() ).hexdigest()

# Create ssl context with:
#           PROTOCOL_TLSv1_1    fail
#           PROTOCOL_TLSv1_2    ok
#           PROTOCOL_TLS_CLIENT ok
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(ca_cert)
#context.load_cert_chain(client_cert, client_key)

the_user_dict = {"connected":       False,
                 "disconnected":    False,
                 "subscribed":      False,
                 "unsubscribed":    False
                 }

# Alternative to using ssl context but throws the exact same error
# client.tls_set(ca_certs=ca_cert, certfile=client_cert, keyfile=client_key, tls_version=ssl.PROTOCOL_TLSv1)

client = paho.Client(userdata=the_user_dict)
client.username_pw_set(username=USER_NAME, password=PASS_WORD)
client.tls_set_context(context)
client.tls_insecure_set(False)  # True: open to impersonating attack.

#client.connect_async(host=HOSTNAME, port=PORT, keepalive=60)
#client.loop_forever()

time_stamp_0 = time.time()

def on_log(client, userdata, level, buf):
    now = time.time()
    print("log %.2f: " % (now - time_stamp_0), buf)

def on_connect(client, userdata, flags, rc):
    print("OnConnect: connected with result code ", str(rc))
    client.subscribe("topic1", qos=2)
    if type(userdata) is dict:
        conn_state = userdata.get("connected", None)
        disc_state = userdata.get("disconnected", None)
        if conn_state == False and disc_state == False:
            userdata["connected"] = True
        else:
            print("Error, OnConnect not in right state ...")
    else:
        print("Error, OnConnect no userdata ...")

def on_disconnect(client, userdata, rc):
    print("OnDisconnect: disconnected with result code ", str(rc))
    if type(userdata) is dict:
        conn_state = userdata.get("connected", None)
        disc_state = userdata.get("disconnected", None)
        if conn_state == True and disc_state == False:
            userdata["disconnected"] = True
        else:
            print("Error, OnDisconnect not in right state...")
    else:
        print("Error, OnDisconnect no userdata...")

def on_publish(client, userdata, mid ):
    now = time.time()
    print("OnPublish: mid ", mid)
    pub_rec = userdata.get("pub-record", None)
    if type(pub_rec) is dict:
        pub_stamp = pub_rec.get("pub-stamp", None)
        pub_mid = pub_rec.get("pub-mid", None)
        if pub_stamp is None:
            print("Error, OnPublish no pub-stamp")
            pub_stamp = 0
        if pub_mid is not None:
            if pub_mid == mid:
                flight_time = now - pub_stamp
                print("OnPublish flight time: ", "%.3f" % flight_time)
            else:
                print("Error, OnPublish mid mismatch. pub_mid ", pub_mid, " mid ", mid)
        else:
            print("Error, OnPublish no pub_mid")
    else:
        print("Error, OnPublish no pub_rec ...")

def on_message(client, userdata, message):
    if type(userdata) is dict:
        conn_state = userdata.get("connected", None)
        disc_state = userdata.get("disconnected", None)
        if conn_state == True and disc_state == False:
            pass # userdata["disconnected"] = True
        else:
            print("Error, OnMessage not in right state ...")
    else:
        print("Error, OnMessage no userdata ...")

    print("OnMessage: message received ", str(message.payload.decode()))
    print("OnMessage: message topic=", message.topic)
    print("OnMessage: message qos=", message.qos)
    print("OnMessage: message retain flag=", message.retain)

client.on_log=on_log
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_publish=on_publish
client.on_message=on_message

rc = client.connect(host=HOSTNAME, port=PORT, keepalive=30)
print("Main connect: rc type: ", type(rc), "  rc value: ", rc)

#try:
#    client.loop_forever(timeout=30)
#    print("ok")
#except:
#    print("exception")

client.loop_start()
time.sleep(10)

pub_send_stamp = time.time()
pub_rec = { "pub-stamp": pub_send_stamp }
the_user_dict["pub-record"] = pub_rec
pub_info = client.publish("topic1", payload="abcd1234", qos=2)
pub_rec["pub-mid"] = pub_info.mid
print("Main Published mid ", pub_info.mid)
if pub_info.rc == 0:
    while True:
        if pub_info.is_published():
            break
        if time.time() - pub_send_stamp > 30:
            break
        time.sleep(0.01) # 10ms
print("Main Published in ", "%.3f" % (time.time() - pub_send_stamp))

time.sleep(100)
client.disconnect()
time.sleep(2)
client.loop_stop()
time.sleep(2)


