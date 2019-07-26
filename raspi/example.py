# Example code for IMRT100 robot project


import imrt_robot_serial
import signal
import time


# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()


# Open serial port, exit if serial port cannot be opened
connected = motor_serial.connect()
if not connected:
    print("Exiting program")
    sys.exit()

    
# Spin receive thread
motor_serial.run()


# Now we will send some motor commands until our motor_serial object tells us that it's time to exit.
# The motor_serial object will inform us when it's time to exit the program
# say if the program is terminated by the user
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :


    ##########################################################
    # This is where your code goes
    # We have provided an example to give you a starting point

    speed_motor_1 = 300
    speed_motor_2 = 150

    motor_serial.sendCommand(speed_motor_1, speed_motor_2)

    
    time.sleep(0.1)


    
    ##########################################################
    ##########################################################




print("Goodbye")
