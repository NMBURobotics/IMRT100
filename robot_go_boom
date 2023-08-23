#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Example code for IMRT100 robot project


# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys
import random
from playsound import playsound
playsound('barbie.mp3')

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 100
TURNING_SPEED = 100
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
        
        

def turn_robot(direction, duration):
    
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        time.sleep(0.10)

        
        
        



# We want our program to send commands at 10 Hz (10 commands per second)
execution_frequency = 100 #Hz
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
    print("Dist hoyre:", dist_1, "   Dist venstre:", dist_2 "   Dist foran1:", dist_3 "   Dist foran2:", dist_4)

    # Check if there is an obstacle in the way
    if dist_1>50 and dist_2>50 and dist_3>50: 
        stop_robot(30)
        #play song
        
    
    elif dist_1>50: 
        drive_robot(FORWARDS,0.3)
        turn_robot(RIGHT,1)
    
    elif dist_1<10 and dist_3<10:
        turn_robot(LEFT,1)
        
    elif dist_1<10 and dist_3<10 and dist_2<10: 
        turn_robot(RIGHT,1)
        turn_robot(RIGHT,1)
    elif dist_3>10 or dist_4>10:
        turn_robot(RIGHT,1)
        
    
        

    else:
        # If there is nothing in front of the robot it continus driving forwards
        drive_robot(FORWARDS, 0.1)
        gain = 8
        speed_motor_1 = dist_1 * gain
        speed_motor_2 = dist_2 * gain
        motor_serial.send_command(speed_motor_1, speed_motor_2)
        
        
        
        


                



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


# In[2]:





# In[ ]:




