import RPi.GPIO as GPIO
import time

def duty_cycle_from_angle(angle):
    duty_cycle = angle/20.+2.
    return duty_cycle

servo_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)
try:
  while True:
    pwm.ChangeDutyCycle(duty_cycle_from_angle(0))
    time.sleep(1.0)
    pwm.ChangeDutyCycle(duty_cycle_from_angle(180))
    time.sleep(1.0)
except KeyboardInterrupt:
  print("Terminated by user")
finally:
  pwm.stop()
  GPIO.cleanup()
