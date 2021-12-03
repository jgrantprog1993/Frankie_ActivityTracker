from gpiozero import LED, Button
import RPi.GPIO as GPIO
from signal import pause
from time import sleep     # Import sleep Library
import os
import time
from datetime import datetime

now = datetime.now() # current date and time
led_Red = LED(21)
led_Green = LED(12)
led_Blue = LED(23)


GPIO.setup(18, GPIO.IN)    # set GPIO25 as input (button)  

button = Button(22)

date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
print("date and time:",date_time)	
pressCount = 1

while True:
 if GPIO.input(18):
    GPIO.output(23,GPIO.HIGH)

    button.wait_for_press() 
    print(f'pressCount {pressCount}') # print frame number to console
    sleep(2)
    if pressCount%2 == 1:
      print(f'green on')
      GPIO.output(12,GPIO.HIGH)
      time.sleep(1)
      os.system(f'gpspipe -w -P -o TestGPS{pressCount}_{date_time}.txt')
    
      
    else:
      print(f'red on')
      GPIO.output(12,GPIO.LOW)
      GPIO.output(21,GPIO.HIGH)
      sleep(2)
      GPIO.output(21,GPIO.LOW)
    
    
    pressCount+=1

              