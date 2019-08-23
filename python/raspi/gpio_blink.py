import RPi.GPIO as GPIO
import time

LED_PIN = 2

# BCM pin naming
GPIO.setmode(GPIO.BCM)

# Turn off GPIO warnings
GPIO.setwarnings(False)

# Set LED pin to output
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    # Loop until user terminates program
    while True:
        
        # Switch LED on
        GPIO.output(LED_PIN, GPIO.HIGH)
        #print("LED on")
        time.sleep(1)

        # Switch LED off
        GPIO.output(LED_PIN, GPIO.LOW)
        #print("LED off")
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Terminated by user")

finally:
    # Cleanup
    GPIO.cleanup()
    print("Goodbye")
