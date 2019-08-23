# Example code for IMRT100 robot project


# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys
import random

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 200
TURNING_SPEED = 173
STOP_DISTANCE = 25


def stop_robot(duration):

    iterations = int(duration * 10)
    
    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.10)



def drive_robot(direction, duration):
    
    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, speed)
        time.sleep(0.10)



def turn_robot_90_degrees_right():

    direction = 1
    iterations = 1
    
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        time.sleep(0.10)

def turn_robot_90_degrees_left():

    direction = -1
    iterations = 1
    
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        time.sleep(0.05)

def turn_robot_180_degrees():

    direction = 1
    iterations = 16
    
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        time.sleep(0.10)




# We want our program to send commands at 10 Hz (10 commands per second)
execution_frequency = 10 #Hz
execution_period = 1. / execution_frequency #seconds


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


# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :


    ###############################################################
    # This is the start of our loop. Your code goes below.        #
    #                                                             #
    # An example is provided to give you a starting point         #
    # In this example we get the distance readings from each of   #
    # the two distance sensors. Then we multiply each reading     #
    # with a constant gain and use the two resulting numbers      #
    # as commands for each of the two motors.                     #
    #  ________________________________________________________   #
    # |                                                        |  #
    # V                                                           #
    # V                                                           #
    ###############################################################






    # Get and print readings from distance sensors
    dist_1 = motor_serial.get_dist_1()
    dist_2 = motor_serial.get_dist_2()
    dist_3 = motor_serial.get_dist_3()
    dist_4 = motor_serial.get_dist_4()

    print("Bak:", dist_1, "Venstre:", dist_2, "Høyre:", dist_3,"Foran:", dist_4)

    # Check if there is an obstacle in the way
    if dist_4 < STOP_DISTANCE:
        # There is an obstacle in front of the robot
        # First let's stop the robot forc 1 second
        print("Obstacle!")
        #stop_robot(1)

        # Reverse for 0.5 second
        # drive_robot(FORWARDS, 0.5)

        # Turn 90 degrees righj
        #turn_robot_180_degrees()
        turn_robot_90_degrees_left()
    if dist_3 > 50 and dist_1 > 30:
            '''
            direction_h = 1
            iterations_h = int((dist_3/30))
            print("Mye",iterations_h)
    
            for i in range(iterations_h):
                motor_serial.send_command(TURNING_SPEED * direction_h, -TURNING_SPEED * direction_h)
                time.sleep(0.10)
            '''
            fortsett = True
            while(fortsett):
                direction_h = 1
                print("Mye")
                motor_serial.send_command(TURNING_SPEED * direction_h, -TURNING_SPEED * 0)
                dist_3 = motor_serial.get_dist_3()
                dist_1 = motor_serial.get_dist_1()
                print(dist_3)
                if dist_3 < 45:
                    fortsett = False
                time.sleep(0.50)
    elif dist_3 > (dist_1 - 10):
        
        turn_robot_90_degrees_right()
        drive_robot(FORWARDS, 0.1)
        print("Høyre")
    elif dist_1 > (dist_3 - 15):
        if dist_3 < STOP_DISTANCE:
            turn_robot_90_degrees_left()
            print("Justering vegg")
            time.sleep(0.10)
        else:
            turn_robot_90_degrees_left()
            drive_robot(FORWARDS, 0.1)
            print("Venstre")

    else:
        # If there is nothing in front of the robot it continus driving forwards
        drive_robot(FORWARDS, 0.1)

    '''
    elif dist_3 > (gammel_venstre+30):
        turn_robot_90_degrees_left()
        gammel_venstre = 100
        print("Sving høyre", dist_3)
    '''
        



        
                



    ###############################################################
    #                                                           A #
    #                                                           A #
    # |_________________________________________________________| #
    #                                                             #
    # This is the end of our loop,                                #
    # execution continus at the start of our loop                 #
    ###############################################################
    ###############################################################





# motor_serial has told us that its time to exit
# we have now exited the loop
# It's only polite to say goodbye
print("Goodbye")
