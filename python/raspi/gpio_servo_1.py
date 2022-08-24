import RPi.GPIO as GPIO
import time


servo_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

try:
  while True:
    pwm.ChangeDutyCycle(4)
    time.sleep(1.0)
    pwm.ChangeDutyCycle(8)
    time.sleep(1.0)
except KeyboardInterrupt:
  print("Terminated by user")
finally:
  pwm.stop()
  GPIO.cleanup()
