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
TURN_SPEED_RIGHT = 180
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
    iterations = 1
    
    for i in range(iterations):
        motor_serial.send_command(TURN_SPEED_RIGHT * direction, -TURN_SPEED_RIGHT * direction)
        time.sleep(0.1)

def turn_robot_mange_degrees_right():

    direction = 1
    iterations = 8
    
    for i in range(iterations):
        motor_serial.send_command(TURN_SPEED_BIG * direction, -TURN_SPEED_BIG * direction)
        time.sleep(0.1)


def turn_robot_90_degrees_left():

    direction = -1
    iterations = 1
    
    for i in range(iterations):
        motor_serial.send_command(TURN_SPEED_LEFT * direction, -TURN_SPEED_LEFT* direction)
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
    dist_1 = motor_serial.get_dist_1()
    dist_2 = motor_serial.get_dist_2()
    dist_3 = motor_serial.get_dist_3()
    dist_4 = motor_serial.get_dist_4()

    print("Høyre bak:", dist_1, "Høyre skrå:", dist_2, "Høyre foran:", dist_3,"Midt foran:", dist_4)
        
    if dist_3 == 255 and dist_2 < 30 and dist_1 < 30:
        print("Feilretting")
        turn_robot_90_degrees_left()
        dist_3 = motor_serial.get_dist_3()

    if dist_4 < 25: 
        turn_robot_90_degrees_left()
        print("Justering foran")
        time.sleep(0.1)
    
    elif dist_2 < 12 or dist_3 < 5:
        turn_robot_90_degrees_left()
        print("Justering vegg venstre")
        time.sleep(0.10)
          
    elif dist_3 > 50 and dist_1 < 30:
        drive_robot(FORWARDS, 0.5)
        turn_robot_mange_degrees_right()
        drive_robot(FORWARDS, 1.0)
        print("Skarp sving, avstand", dist_3)
        
        dist_3 = motor_serial.get_dist_3()
        if dist_3 > 60:
            drive_robot(FORWARDS, 1.2)
            turn_robot_mange_degrees_right()
            drive_robot(FORWARDS, 0.8)
            print("Skarp sving 2, avstand", dist_3)
        else:
            drive_robot(FORWARDS, 0.1)

    elif dist_3 > 25 and dist_1 > 25 and dist_4 > 30 and dist_2 > 40:
        turn_robot_90_degrees_right()
        turn_robot_90_degrees_right()
        turn_robot_90_degrees_right()
        fortsett = True
        gi_deg = 0
        while(fortsett):
            gi_deg += 1
            drive_robot(FORWARDS, 0.2)
            if gi_deg % 4 == 0:
                turn_robot_90_degrees_right()
            dist_4 = motor_serial.get_dist_4()
            dist_2 = motor_serial.get_dist_2()
            dist_3 = motor_serial.get_dist_3()
            print("FINN VEGG", gi_deg, dist_4)
            if dist_4 < 30 or dist_3 < 25 or dist_2 < 25 or gi_deg > 16:
                print("Gi deg")
                fortsett = False
                
    elif dist_3 > (dist_1) or dist_3 > 50:
        turn_robot_90_degrees_right()
        drive_robot(FORWARDS, 0.1)
        print("Liten justering høyre: ", dist_3)

    elif dist_1 > (dist_3):
        turn_robot_90_degrees_left()
        drive_robot(FORWARDS, 0.1)
        print("Venstre")
        
        
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
    '''
    elif dist_3 > 25 and dist_1 > 25 and dist_4 > 30 and dist_2 > 40:
        turn_robot_90_degrees_right()
        turn_robot_90_degrees_right()
        turn_robot_90_degrees_right()
        fortsett = True
        gi_deg = 0
        while(fortsett):
            gi_deg += 1
            drive_robot(FORWARDS, 0.05)
            if gi_deg % 4 == 0:
                turn_robot_90_degrees_right()
            dist_4 = motor_serial.get_dist_4()
            dist_2 = motor_serial.get_dist_2()
            dist_3 = motor_serial.get_dist_3()
            print("FINN VEGG", gi_deg, dist_4)
            if dist_4 < 30 or dist_3 < 25 or dist_2 < 25 or gi_deg > 16:
                print("Gi deg")
                fortsett = False
    '''




# motor_serial has told us that its time to exit
# we have now exited the loop
# It's only polite to say goodbye
print("Goodbye")
