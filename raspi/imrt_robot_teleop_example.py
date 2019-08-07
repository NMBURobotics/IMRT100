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




# Robot dimentions
ROBOT_WIDTH = 0.40 # m




# Function to make the robot move
def move(pos):

    # use pos.x, pos.y and pos.distance to determin vx and wz
    vx = pos.distance * (1,-1)[pos.y > 0]
    wz = pos.x
    print(vx, wz)

    # calculate motor commands
    v1 = ( 2 * vx - ROBOT_WIDTH * wz ) / 2 * 400
    v2 = ( 2 * vx + ROBOT_WIDTH * wz ) / 2 * 400
    
    # send motor commands
    motor_serial.sendCommand(int(v1), int(v2))




# Function to make the robot stop
def stop():
    motor_serial.sendCommand(0, 0)




##################################################
# This is where our program will start executing #
#################################################

if __name__ == '__main__':

      
    # Create motor serial object
    motor_serial = imrt_robot_serial.IMRTRobotSerial()


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
   
    

    
    # Loop forever
    while not motor_serial.shutdown_now:

        v1 = 0
        v2 = 0
        
        if bd.is_pressed:

            # use pos.x, pos.y and pos.distance to determin vx and wz
            vx = bd.position.distance * (1,-1)[bd.position.y > 0]
            wz = bd.position.x * (1,-1)[bd.position.y > 0]
            print(vx, wz)

            # calculate motor commands
            v1 = ( 2 * vx - ROBOT_WIDTH * wz ) / 2 * 400
            v2 = ( 2 * vx + ROBOT_WIDTH * wz ) / 2 * 400


            
        # send motor commands
        motor_serial.sendCommand(int(v1), int(v2))


        # sleep for 0.05 seconds
        time.sleep(0.05)



    # End of program
    print("Goodbye")
            




