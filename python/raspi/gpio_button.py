import RPi.GPIO as GPIO
import time

LED_PIN = 2
BUTTON_PIN = 4

# Function for debouncing button
def debounce(pin, prev_state):
    current_state = GPIO.input(pin)
    if current_state != prev_state:
        time.sleep(0.05)
        current_state = GPIO.input(pin)

    return current_state


# BCM pin naming
GPIO.setmode(GPIO.BCM)

# Turn of GPIO warnings
GPIO.setwarnings(False)

# Setup output and input pins
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initial state of LED
led_on = False
GPIO.output(LED_PIN, led_on)

# Initial prev button state
prev_button_pressed = GPIO.input(BUTTON_PIN)

try:
    # Loop until user terminates program
    while True:

        # Read button state using debounce function
        current_button_pressed = GPIO.input(BUTTON_PIN)

        # Toggle LED when button goes from low to high
        if current_button_pressed and not prev_button_pressed:
            led_on = not led_on
            GPIO.output(LED_PIN, led_on)
            print("LED on:", led_on)

        # This iteration's current button is next iteration's prev button
        prev_button_pressed = current_button_pressed

        time.sleep(0.05)


except KeyboardInterrupt:
    print("Terminated by user")

finally:
    GPIO.cleanup()
    print("Goodbye")
