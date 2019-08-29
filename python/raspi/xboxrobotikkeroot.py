from __future__ import print_function
import imrt_xbox
import imrt_robot_serial
import sys
import signal
import time

motor_serial = imrt_robot_serial.IMRTRobotSerial()

try:
    motor_serial.connect("/dev/ttyACM0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

motor_serial.run()
    
# Format floating point number to string format -x.xxx
def fmtFloat(n):
    return '{:6.3f}'.format(n)

# Print one or more values without a line feed
def show(*args):
    for arg in args:
        print(arg, end="")

# Print true or false value based on a boolean, without linefeed
def showIf(boolean, ifTrue, ifFalse=" "):
    if boolean:
        show(ifTrue)
    else:
        show(ifFalse)

# Instantiate the controller
joy = imrt_xbox.IMRTxbox()

vx_gain = 1
wz_gain = 2


# Show various axis and button states until Back button is pressed
print("Xbox controller sample: Press Back button to exit")
try:
    while not joy.getBack():


        vx = -(vx_gain * joy.getLeftY())
        wz = -(wz_gain * joy.getRightX())
        
        turn_left = joy.getLeftBumper()
        turn_right = joy.getRightBumper()
        print(turn_right, turn_left)

        if turn_left:
            motor_serial.send_command(-400,400)
            print("turn left")
        elif turn_right:
            motor_serial.send_command(400,-400)
            print("turn right")

        else:
        # calculate motor commands
            vel1 = (vx - 0.40 * wz / 2) * 400
            vel2 = (vx + 0.40 * wz / 2) * 400

            motor_serial.send_command(int(vel1),int(vel2))
            print("drive")
        time.sleep(0.005)
    
except KeyboardInterrupt:
    print("Terminated by user")

finally:
    # Close out when done
    joy.shutdown()
    motor_serial._shutdown()

