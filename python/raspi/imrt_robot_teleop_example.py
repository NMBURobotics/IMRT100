# Example code for teleoperating the IMRT100 robot
# using an app called Blue Dot
#
# This is an example of an event-driven program
# The program will wait for something to happen in the
# Blue Dot app on the paired device. When the user presses the
# blue dot in the Blue Dot app, it will trigger a function call
# in this program.


# Import some modules that we will need
import imrt_robot_serial
import signal
import sys
import bluedot
import time

# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()

count = 0


def rotated(rotation):
    global count
    count += rotation.value
    print(rotation.value)

    motor_serial.send_command(400 * rotation.value, -400 * rotation.value)
    time.sleep(0.1)
    

# Robot dimentions
ROBOT_WIDTH = 0.40 # m






##################################################
# This is where our program will start executing #
#################################################

if __name__ == '__main__':

      



    # Open serial port. Exit if serial port cannot be opened
    try:
        motor_serial.connect("/dev/ttyACM0")
    except:
        print("Could not open port. Is your robot connected?\nExiting program")
        sys.exit()
    
        
    # Start serial receive thread
    motor_serial.run()
    
    
    # Create bluedot object
    bd = bluedot.BlueDot()
    bd.color = "red"
    bd.when_rotated = rotated

    vx_gain = 1
    wz_gain = 2
   
    

    
    # Loop forever
    while not motor_serial.shutdown_now:

        v1 = 0
        v2 = 0
        
        if bd.is_pressed and bd.position.distance < 0.8:

            # use pos.x, pos.y and pos.distance to determin vx and wz
            vx = vx_gain * bd.position.distance * (-1,1)[bd.position.y > 0]
            wz = wz_gain * bd.position.x * (1,-1)[bd.position.y > 0]
            print(vx, wz)

            # calculate motor commands
            v1 = (vx - ROBOT_WIDTH * wz / 2) * 700
            v2 = (vx + ROBOT_WIDTH * wz / 2) * 700

            print("sending commands")
            motor_serial.send_command(int(v1), int(v2))

        elif bd.is_pressed:
            pass
        else:
            motor_serial.send_command(0, 0)
            
    

        


            
        #send motor commands
        



        # sleep for 0.05 seconds
        time.sleep(0.1)



    # End of program
    print("Goodbye")
            




