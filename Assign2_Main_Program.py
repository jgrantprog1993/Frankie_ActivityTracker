#################
# Name: Jason Grant
# ID: 12430732
# Description: IOT Assignment 2: Main Program,  (main thread)
#################

##### #import all libraries needed# #####
import serial
from gpiozero import LED
import RPi.GPIO as GPIO
from time import sleep     
import subprocess
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from urllib.parse import urlparse
import time
import logging
from gpiozero import LED
from picamera import PiCamera
import pandas as pd
import geojson
import BlynkLib

##### #Initialise Camera# #####
camera = PiCamera()

##### #Blynk Setup# #####
BLYNK_AUTH = '_1YBrbat_TJksBX_p4ni9jz5gr3q62so'
# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

logging.basicConfig(level=logging.INFO)

# parse mqtt url for connection details
#url_str = 'mqtt://broker.emqx.io:8883/grantj2/home'
#print(url_str)
#url = urlparse(url_str)
#base_topic = url.path[1:]

# Connect
#if (url.username):
 #  auth1 = {'username':url.username, 'password':url.password}


now = datetime.now() # current date and time

##### #Initialise GPIO -  Buttons & LEDS# #####
led_Red = LED(21)
led_Green = LED(12)
led_Blue = LED(23)

GPIO.setup(18, GPIO.IN)                                     # set as input (button)  
GPIO.setup(19, GPIO.IN)                                     # set as input (button)  
GPIO.setup(22, GPIO.IN)                                     # set as input (button) 
GPIO.setup(6, GPIO.IN)                                      # set as input (button) 

date_timeStart = now.strftime("%m_%d_%Y_%H_%M_%S")
print("date and time:",date_timeStart)	

##### #Initialising press count# #####
##This in determines the state of the application Run/Waiting for run.
pressCount = 1

##### #Function Definitions# #####

##### #Function for action on button press# #####
def my_callback(channel):  
    print ("Count Inc")
    global pressCount
    pressCount+=1

##### #Translates list of arrays into the conrect .json / .geojson format# #####
## reference -> https://newbedev.com/pandas-to-geojson-multiples-points-features-with-python
def data2geojson(df):
    features = []
    insert_features = lambda X: features.append(
            geojson.Feature(geometry=geojson.Point((X["lat"],
                                                    X["long"]))))
    df.apply(insert_features, axis=1)
    with open('map1.geojson', 'w', encoding='utf8') as fp:
        geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)

##### #function that waits for button press and if pressed take picture# #####
def my_callback2(channel):  
    global frame
    fileLoc = f'/home/pi/Assignment_2/DB_Folder/Photo_frame_1.jpg' # set the location of image file and current time
    currentTime = now.strftime("%H:%M:%S")
    camera.capture(fileLoc) # capture image and store in fileLoc
    print(f'frame {frame} taken at {currentTime}') # print frame number to console
    print("TOOK A PICTURE")
    frame += 1
    camera.close

##### #Initialising frame var for picture# #####
frame = 1

##### #GPIO event detection 22 -> inc presscount, 6 -> takes picture# #####
GPIO.add_event_detect(22, GPIO.FALLING, callback=my_callback, bouncetime=300)  
GPIO.add_event_detect(6, GPIO.FALLING, callback=my_callback2, bouncetime=300)

##### #Initilaising reading in from serial for the GPS# #####
gps = serial.Serial("/dev/ttyACM0", baudrate=9600)
x,y = 0,0

global data_Formatted

data_Formatted = [ [None]*x for i in range(y) ]
col = ['lat','long']

while True:
    blynk.run()                                                 ## Running Blynk app
    if GPIO.input(18):                                          ## Life bit
        GPIO.output(23,GPIO.HIGH)                               ## if power turn on the blue light
    
        sleep(.1)
        virtualPinV0 = pressCount%2                             ##virtualpin 0 is for Blynk app to show if we are 'Tracking' or idle
        if pressCount%2 == 1:                                   ##If we are 'tracking, then execute
            
            blynk.virtual_write(0, virtualPinV0 )
            date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
            ##print(f'green on')
            GPIO.output(12,GPIO.HIGH)                           ##Green LED to Shine
            time.sleep(.1)
            line = gps.readline()                               ##Read in from GPS serial
          
            data = line.decode('utf8').split(",")               ##converting strings into a list

            ##### #Taking in the List and extracting L and LON data # #####
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

                    ##### #Creating/Appending List of Coords # #####
                    data_Formatted.append([lat, lon])
                    print(data_Formatted)                                   ##Visual test to see coords coming in
                    
                    ##### #Writing results to Blynk # #####
                    blynk.virtual_write(5, lat)
                    blynk.virtual_write(6, lon)
                    blynk.virtual_write(2, lon, lat)

                    print(f"{lat:.5f},{lon:.5f} , {date_time_updating} ")   ##Visual test to see results

                    ##### #Writing results to .txt file # #####
                    file1 = open(f'ResultsFolder/GPS_TrackerData_{pressCount}_{date_time}.txt', 'a')
                    file1.write(f"{lat:.5f} {lon:.5f} {date_time_updating} \n")                     ##.5f formats to 5 decimal places
                    file1.close
                    file2 = open(f'DB_Folder/GPS_TrackerData_{pressCount}_{date_time}.txt', 'a')
                    file2.write(f"Lat: {lat:.5f}, Lon: {lon:.5f}, DateTime: {date_time_updating} \n")
                    file2.close
                    ##### #runs the script below, and passes lat and lon as arguments to that .py program to be used# #####
                    process = subprocess.run(f"python3 thinkspeak_MQTT.py {lat} {lon}", shell = True)

                    
                else:
                    print("No Connection")
                    
                    
        else:
            ##print(f'red on')
            file1.close 
            GPIO.output(12,GPIO.LOW)                                        ##Turns of green LED
            GPIO.output(21,GPIO.HIGH)                                       ##Turns on RED LED to signal process/ logging / Activity stop
            sleep(0.5)
            blynk.virtual_write(0, virtualPinV0 )                           # updateds Blynk
            #print(virtualPinV0)
            process = subprocess.run("python3 Distance_calculator.py", shell=True) ##runs program to calc the summary of the activity
            df = pd.DataFrame(data_Formatted, columns=col) 
            data2geojson(df)
            GPIO.output(21,GPIO.LOW)
            blynk.virtual_write(7,f'GPS_TrackerData_{date_time}' )
            logging.info("Activity Complete ! ")
            ##### #runs the script below, which creates map of activity# #####
            process3 = subprocess.run(f"python3 Assign2_NotOnPi/folium_GPS.py", shell = True)
            
            print("Waiting for another Activity Start")
            data_Formatted = []                                            ##resets the list of arrays of the activity, ready to be populated by next activity
            GPIO.wait_for_edge(19, GPIO.FALLING)                            ##wait for reset (Go Again)
            pressCount+=1                                                   ##Starts another activity
            