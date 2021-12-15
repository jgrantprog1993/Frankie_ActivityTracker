#!/usr/bin/python3

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys

from cryptography.fernet import Fernet

def decrypt_payload(payload):
    cypher_key=b'xqi9zRusHkcv3Om050HwX82eMTO-LbeW4YlqVVEzpw8=' #THIS IS VERY INSECURE - SHOULD BE ENV/EXTERNAL VARIABLE
    cypher=Fernet(cypher_key)
    decrypted_payload=cypher.decrypt(payload)
    return(decrypted_payload.decode())

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connection Result: " + str(rc))

def on_message(client, obj, msg):
    print("Topic:"+msg.topic + ",Payload:" + decrypt_payload(msg.payload))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed,  QOS granted: "+ str(granted_qos))

def main():
    mqttc = mqtt.Client()
    mqttc.tls_set("./broker.emqx.io-ca.crt")

    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe

    # parse mqtt url for connection details
    url_str = 'mqtt://broker.emqx.io:8883/grantj2/home'
    url = urlparse(url_str)
    base_topic = url.path[1:]

    # Connect
    if (url.username):
        mqttc.username_pw_set(url.username, url.password)
    print(url.hostname)
    print(url.port)
    mqttc.connect(url.hostname, url.port)

    # Start subscribe, with QoS 1
    mqttc.subscribe(base_topic+"/#", 1)
    mqttc.loop_forever()

    # Continue the network loop, exit when an error occurs
    rc = 0
    while rc == 0:
        rc = mqttc.loop()

    print("rc: " + str(rc))

if __name__ == "__main__":
    main()
