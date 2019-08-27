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
STOP_DISTANCE = 35
TURN_SPEED_RIGHT = 100
TURN_SPEED_LEFT = 100
TURN_SPEED_BIG = 180


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
    iterations = 10
    
    for i in range(iterations):
        motor_serial.send_command(TURN_SPEED_RIGHT * direction, -TURN_SPEED_RIGHT * direction)
        time.sleep(0.1)
        
def turn_robot_90_degrees_left():

    direction = -1
    iterations = 10
    
    for i in range(iterations):
        motor_serial.send_command(TURN_SPEED_LEFT * direction, -TURN_SPEED_LEFT* direction)
        time.sleep(0.1)
        
def adjust_left():

    direction = -1
    iterations = 1
    
    for i in range(iterations):
        motor_serial.send_command(TURN_SPEED_LEFT * direction, -TURN_SPEED_LEFT* direction)
        time.sleep(0.1)

def adjust_right():

    direction = 1
    iterations = 1
    
    for i in range(iterations):
        motor_serial.send_command(TURN_SPEED_RIGHT * direction, -TURN_SPEED_RIGHT* direction)
        time.sleep(0.1)




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
    right_rear = motor_serial.get_dist_1()
    left_front = motor_serial.get_dist_2()
    right_front = motor_serial.get_dist_3()
    middle_front = motor_serial.get_dist_4()
    a = (right_front) - (right_rear)

    print("Right rear:", right_rear, "Left front:", left_front, "Right front:", right_front,"Middle front:", middle_front)
    print("dette er a:",a)

    # Check if there is an obstacle in the way
    if middle_front < 25:
        time.sleep(0.1)
        turn_robot_90_degrees_left()
        print("Vegg foran")
    
    elif a > -8 and a < 8:
        drive_robot(FORWARDS, 0.5)
        print("rett")

    elif right_front < right_rear:
        adjust_left()
        print("Adjust left")
    elif right_front > right_rear:
        adjust_right
        print("Adjust right")
        
    elif right_front > 100:
        drive_robot(FORWARDS, 0.8)
        turn_robot_90_degrees_right()
        drive_robot(FORWARDS, 0.2)
        right_front = motor_serial.get_dist_3()
        print("right front")
        if right_front > 100:
            drive_robot(FORWARDS, 0.8)
            turn_robot_90_degrees_right()
            drive_robot(FORWARDS, 0.2)        
            
    else:
        drive_robot(FORWARDS, 0.1)

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
