# Example code for IMRT100 robot project


# Import some modules that we need
import imrt_robot_serial
import signal
import time


# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()


# Open serial port. Exit if serial port cannot be opened
if not motor_serial.connect("/dev/ttyACM0"):
    print("Exiting program")
    sys.exit()

    
# Start serial receive thread
motor_serial.run()


# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :


    ###############################################################
    # This is the start of our loop. Your code goes below         #
    # An example is provided to give you a starting point         #
    #  ________________________________________________________   #
    # |                                                        |  #
    # V                                                           #
    # V                                                           #
    ###############################################################


    # Preparing commands for our motors
    speed_motor_1 = 300
    speed_motor_2 = 150


    # Send commands to motor
    motor_serial.sendCommand(speed_motor_1, speed_motor_2)


    # Sleep for 0.1 seconds
    time.sleep(0.1)


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
