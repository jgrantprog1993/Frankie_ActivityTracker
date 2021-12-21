#!/usr/bin/python3
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from urllib.parse import urlparse
import sys
import time
import json

from cryptography.fernet import Fernet

def encrypt_payload(payload):
    #HAVING A HARD CODED KEY IS INSECURE  - SHOULD BE ENV/EXTERNAL VARIABLE
    cypher_key=b'xqi9zRusHkcv3Om050HwX82eMTO-LbeW4YlqVVEzpw8=' 
    cypher=Fernet(cypher_key)
    encrypted_payload=cypher.encrypt(payload.encode('utf-8'))
    return(encrypted_payload.decode())


# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connection Result: " + str(rc))

def on_publish(client, obj, mid):
    print("Message ID: " + str(mid))

mqttc = mqtt.Client()
mqttc.tls_set("./broker.emqx.io-ca.crt")

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish


# parse mqtt url for connection details
url_str = 'mqtt://broker.emqx.io:8883/grantj2/home'
print(url_str)
url = urlparse(url_str)
base_topic = url.path[1:]
auth=None

# Connect
if (url.username):
    auth = {'username':url.username, 'password':url.password}


mqttc.connect(url.hostname, url.port)
mqttc.loop_start()
temp=1
humidity=2
pressure=3
    # Publish a message
while True:
    
    print("Got Here 1")
    temp+=1
    humidity+=1
    pressure+=1
    #Create JSON strings
    temp_sensor=json.dumps({"temperature":temp, "timestamp":time.time()}) 
    humidity_sensor=json.dumps({"humidity":humidity, "timestamp":time.time()}) 
    pressure_sensor=json.dumps({"pressure":pressure, "timestamp":time.time()}) 
    print("Got Here 2")
    #Crate array of MQTT messages
    temp_msg={'topic': base_topic +"/temperature", 'payload':encrypt_payload(temp_sensor)}
    hum_msg={'topic':base_topic +"/humidity", 'payload':encrypt_payload(humidity_sensor)}
    pre_msg={'topic':base_topic +"/pressure", 'payload':encrypt_payload(pressure_sensor)}
    msgs=[temp_msg,hum_msg, pre_msg]
    print("Got Here 3")
    #Publish array of messages
    
    
    mqttc.publish(base_topic +"/temperature", encrypt_payload(temp_sensor), 1)
    mqttc.publish(base_topic +"/humidity", encrypt_payload(humidity_sensor), 1)
    mqttc.publish(base_topic +"/pressure", encrypt_payload(pressure_sensor), 1)
    #mqttc.publish(hum_msg)
    #mqttc.publish(pre_msg)
    

    #time.sleep(5)
    print("published1")
    #time.sleep()

