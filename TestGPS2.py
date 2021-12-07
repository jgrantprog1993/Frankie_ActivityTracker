import serial
from gpiozero import LED, Button
import RPi.GPIO as GPIO
from signal import pause
from time import sleep     # Import sleep Library
import os
import subprocess
import time
from datetime import datetime

now = datetime.now() # current date and time
led_Red = LED(21)
led_Green = LED(12)
led_Blue = LED(23)

GPIO.setup(18, GPIO.IN)    # set as input (button)  
GPIO.setup(19, GPIO.IN)    # set as input (button)  
GPIO.setup(22, GPIO.IN)    # set as input (button) 
##button = Button(22)
date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
print("date and time:",date_time)	

pressCount = 1

def my_callback(channel):  
    print ("Count Inc")
    global pressCount
    pressCount+=1

  
GPIO.add_event_detect(22, GPIO.FALLING, callback=my_callback, bouncetime=300)  

gps = serial.Serial("/dev/ttyACM0", baudrate=9600)

while True:
    if GPIO.input(18):
        GPIO.output(23,GPIO.HIGH)

        ##button.wait_for_press()
        ##pressCount+=1
        ##print(f'pressCount {pressCount}') # print frame number to console
        sleep(.1)
        if pressCount%2 == 1:
            ##print(f'green on')
            GPIO.output(12,GPIO.HIGH)
            time.sleep(.1)
            line = gps.readline()
            ##print(f"->{line}")
            data = line.decode('utf8').split(",")
            ##print(f"->{data}")
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

                    print(f"lat:{lat:.5f}, lon:{lon:.5f}")
            
                else:
                    print("No Connection")
        else:
            ##print(f'red on')
            GPIO.output(12,GPIO.LOW)
            GPIO.output(21,GPIO.HIGH)
            sleep(2)
            GPIO.output(21,GPIO.LOW)
            GPIO.wait_for_edge(19, GPIO.FALLING)
            pressCount+=1
            