import serial
from gpiozero import LED, Button
import RPi.GPIO as GPIO
from signal import pause
from time import sleep     # Import sleep Library
import os
import subprocess
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from urllib.parse import urlparse
import sys
import time
import json
import logging
from dotenv import dotenv_values
from gpiozero import LED, Button
from signal import pause
from picamera import PiCamera
import smtplib


camera = PiCamera()
import BlynkLib

BLYNK_AUTH = '_1YBrbat_TJksBX_p4ni9jz5gr3q62so'
# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)


# parse mqtt url for connection details
#url_str = 'mqtt://broker.emqx.io:8883/grantj2/home'
#print(url_str)
#url = urlparse(url_str)
#base_topic = url.path[1:]

# Connect
#if (url.username):
 #  auth1 = {'username':url.username, 'password':url.password}


now = datetime.now() # current date and time
led_Red = LED(21)
led_Green = LED(12)
led_Blue = LED(23)

GPIO.setup(18, GPIO.IN)    # set as input (button)  
GPIO.setup(19, GPIO.IN)    # set as input (button)  
GPIO.setup(22, GPIO.IN)    # set as input (button) 
GPIO.setup(6, GPIO.IN)    # set as input (button) 
##button = Button(22)
date_timeStart = now.strftime("%m_%d_%Y_%H_%M_%S")
print("date and time:",date_timeStart)	

pressCount = 1

def my_callback(channel):  
    print ("Count Inc")
    global pressCount
    pressCount+=1



def my_callback2(channel):  
    global frame
    fileLoc = f'/home/pi/Assignment_2/DB_Folder/Photo_frame_1.jpg' # set the location of image file and current time
    currentTime = now.strftime("%H:%M:%S")
    camera.capture(fileLoc) # capture image and store in fileLoc
    print(f'frame {frame} taken at {currentTime}') # print frame number to console
    print("TOOK A PICTURE")
    frame += 1




frame = 1
GPIO.add_event_detect(22, GPIO.FALLING, callback=my_callback, bouncetime=300)  

GPIO.add_event_detect(6, GPIO.FALLING, callback=my_callback2, bouncetime=300)
gps = serial.Serial("/dev/ttyACM0", baudrate=9600)

while True:
    blynk.run()
    if GPIO.input(18):
        GPIO.output(23,GPIO.HIGH)
        data_gps = {}
        data_gps['coordinates'] = []
        sleep(.1)
        virtualPinV0 = pressCount%2 
        if pressCount%2 == 1:
            
            blynk.virtual_write(0, virtualPinV0 )
            date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
            ##print(f'green on')
            GPIO.output(12,GPIO.HIGH)
            time.sleep(.1)
            line = gps.readline()
          
            data = line.decode('utf8').split(",")
      
            if data[0] == "$GPRMC":
                if data[2]=="A":
                    latgps=float(data[3])
                    if data[4] == "S":
                        latgps = -latgps
                    
                    latdeg = int(latgps/100)
                    latmin = latgps - latdeg*100
                    lat = latdeg+(latmin/60)

                    longps=float(data[5])
                    if data[6] == "W":
                        longps = -longps
                    
                    londeg = int(longps/100)
                    lonmin = longps - londeg*100
                    lon = londeg+(lonmin/60)

                    date_time_updating =data[1]

                    data_gps['coordinates'].append({
                        'Lat': lat,
                        'Lon': lon,
                        'DateTime': date_time_updating
                    })
                    blynk.virtual_write(5, lat)
                    blynk.virtual_write(6, lon)
                    blynk.virtual_write(2, lon, lat)

                    print(f"{lat:.5f},{lon:.5f} , {date_time_updating} ")
              
                    file1 = open(f'ResultsFolder/GPS_TrackerData_{pressCount}_{date_time}.txt', 'a')
                    file1.write(f"{lat:.5f} {lon:.5f} {date_time_updating} \n")
                    file2 = open(f'DB_Folder/GPS_TrackerData_{pressCount}_{date_time}.txt', 'a')
                    file2.write(f"Lat: {lat:.5f}, Lon: {lon:.5f}, DateTime: {date_time_updating} \n")
            
                    process = subprocess.run(f"python3 thinkspeak_MQTT.py {lat} {lon}", shell = True)
                    

                    #Create JSON strings
                    #lat_json=json.dumps({"Lattitude":lat}) 
                    #lon_json=json.dumps({"Longitude":lon}) 
                    #date_time_json=json.dumps({"DateTime":date_time_updating}) 


                    ## Real Time ##
                    ##with open(f'ResultsFolder/GPS_TrackerData_JSON_{pressCount}_{date_time}.txt', 'w') as outfile:
                    ##    json.dump(data_gps, outfile, indent=2)
                    #
                    #with open(f'ResultsFolder/GPS_TrackerData_JSON_{pressCount}_{date_time}.json', 'r+') as outfile:
                    #    json.dump(data_gps, outfile, indent=2)

                    #Create array of MQTT messages
                    #lat_msg={'topic': base_topic +"/lat", 'payload':lat_json}
                    #lon_msg={'topic':base_topic +"/lon", 'payload':lon_json}
                    #dateTime_msg={'topic':base_topic +"/dateTime", 'payload':date_time_json}
                   # msgs=[lat_msg,lon_msg, dateTime_msg]

                    #Publish array of messages
                    #publish.multiple(msgs, hostname=url.hostname, port=url.port)
                    ##print("published")
                    ##sleep(0.7)
                    
                else:
                    print("No Connection")
                    
                    
        else:
            ##print(f'red on')
            file1.close
            GPIO.output(12,GPIO.LOW)
            GPIO.output(21,GPIO.HIGH)
            sleep(0.5)
            blynk.virtual_write(0, virtualPinV0 )
            print(virtualPinV0)
            process = subprocess.run("python3 Distance_calculator.py", shell=True)
            #process.kill
            GPIO.output(21,GPIO.LOW)
            blynk.virtual_write(7,f'GPS_TrackerData_{date_time}' )
            
            GPIO.wait_for_edge(19, GPIO.FALLING)
            pressCount+=1
            