import RPi.GPIO as GPIO
import os
import signal
import time

def buttonCallback(channel):
    print("Button was pressed")
    time.sleep(2)
    if not GPIO.input(19):
        print("...and thats 2 seconds")
        os.system("shutdown now -h")

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(19,GPIO.FALLING,callback=buttonCallback, bouncetime=400)

signal.pause()
GPIO.cleanup()

