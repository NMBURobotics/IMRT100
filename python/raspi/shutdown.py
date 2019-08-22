#!/usr/bin/env python3

import os
import time
import RPi.GPIO as GPIO

DELAY = 4
BUT_PIN = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUT_PIN, GPIO.IN, GPIO.PUD_UP)


print("Listening to shutdown button")
looping = True
last_ok = time.time()


while looping:
    
  current_but = GPIO.input(BUT_PIN)
  
  if current_but:
      last_ok = time.time()

  if time.time() > last_ok + DELAY:
      print("Button shutdown")
      looping = False
      
  time.sleep(0.1)

  
GPIO.cleanup()

print("BYE!")
os.system("shutdown now -h")
