#!/usr/bin/python
#
# http://stackoverflow.com/questions/35621075/mqtt-over-web-socket-in-python

import sys
import paho.mqtt.client as mqtt

def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

mqttc = mqtt.Client(transport='websockets')   
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect("test.mosquitto.org", 8080, 60)

mqttc.subscribe("#", 0)
#mqttc.subscribe("$SYS/#", 0)

mqttc.loop_forever()


# according to http://test.mosquitto.org/
# The server listens on the following ports:
#
#    1883 : MQTT, unencrypted
#    8883 : MQTT, encrypted
#    8884 : MQTT, encrypted, client certificate required
#    8080 : MQTT over WebSockets, unencrypted
#    8081 : MQTT over WebSockets, encrypted
#
# The encrypted ports support TLS v1.2, v1.1 or v1.0 with x509 certificates and 
# require client support to connect. In all cases you should use the certificate 
# authority file mosquitto.org.crt to verify the server connection. Port 8884 
# requires clients to provide a certificate to authenticate their connection. 
# If you wish to obtain a client certificate, please get it touch.


