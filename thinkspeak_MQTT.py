#!/usr/bin/python3
#################
# Name: Jason Grant
# ID: 12430732
# Description: IOT Assignment 2: MQTT publishes to ThinkSpeak
#################

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys
import time
import logging
from dotenv import dotenv_values


#load MQTT configuration values from .env file
config = dotenv_values(".env")

#configure Logging
logging.basicConfig(level=logging.INFO)

# Define event callbacks for MQTT
def on_connect(client, userdata, flags, rc):
    logging.info("Connection Result: " + str(rc))

def on_publish(client, obj, mid):
    logging.info("Message Sent ID: " + str(mid))

mqttc = mqtt.Client(client_id=config["clientId"])

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# parse mqtt url for connection details
url_str = 'mqtt://mqtt3.thingspeak.com:8883'
#print(url_str)
url = urlparse(url_str)
base_topic = url.path[1:]

# Configure MQTT client with user name and password
mqttc.username_pw_set(config["username"], config["password"])
# Load CA certificate for Transport Layer Security
mqttc.tls_set("./broker.thingspeak.crt")

#Connect to MQTT Broker
mqttc.connect(url.hostname, url.port)
mqttc.loop_start()

#Set Thingspeak Channel to publish to
topic = "channels/"+config["channelId"]+"/publish"
lat = sys.argv[1]
lon = sys.argv[2]

# Publish a message to temp every 15 seconds
while True:
    
    try:
        payload=f"field1={lat}&field2={lon}"
        mqttc.publish(topic, payload)
        sys.exit(0)
    except:
        logging.info('Interrupted')
        sys.exit(0)