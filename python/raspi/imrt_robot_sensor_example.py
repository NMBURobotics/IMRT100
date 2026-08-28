# Example code for IMRT100 robot project


# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys


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


    # Get the current time
    iteration_start_time = time.time()



    # Get and print readings from distance sensors
    dist_1 = motor_serial.get_dist_1()
    dist_2 = motor_serial.get_dist_2()
    dist_3 = motor_serial.get_dist_3()
    dist_4 = motor_serial.get_dist_4()
    #print("Dist 1:", dist_1, "   Dist 2:", dist_2, "   Dist 3:", dist_3, "   Dist 4:", dist_4) # Old way to print, not very pretty.
    
    # We want to print the distance readings in a nice way, so that the numbers are aligned
    if (dist_1 < 10):
        dist_1_text = "Dist 1:  "
    elif (dist_1 < 100):
        dist_1_text = "Dist 1: "
    else:
        dist_1_text = "Dist 1:"
    if (dist_2 < 10):
        dist_2_text = "Dist 2:  "
    elif (dist_2 < 100):
        dist_2_text = "Dist 2: "
    else:
        dist_2_text = "Dist 2:"
    if (dist_3 < 10):
        dist_3_text = "Dist 3:  "
    elif (dist_3 < 100):
        dist_3_text = "Dist 3: "
    else:
        dist_3_text = "Dist 3:"
    if (dist_4 < 10):               
        dist_4_text = "Dist 4:  "
    elif (dist_4 < 100):
        dist_4_text = "Dist 4: "
    else:
        dist_4_text = "Dist 4:"   
    print(dist_1_text, dist_1, "   ", dist_2_text, dist_2, "   ", dist_3_text, dist_3, "   ", dist_4_text, dist_4)

    

    # Calculate commands for each motor using sensor readings
    # In this simple example we will multiply each sensor reading
    # with a constant to obtain our commands
    gain = 8
    speed_motor_1 = dist_1 * gain
    speed_motor_2 = dist_2 * gain



    # Send commands to motor
    # Max speed is 400.
    # E.g.a command of 500 will result in the same speed as if the command was 400
    motor_serial.send_command(speed_motor_1, speed_motor_2)



    # Here we pause the execution of the program for the apropriate amout of time
    # so that our loop executes at the frequency specified by the variable execution_frequency
    iteration_end_time = time.time() # current time
    iteration_duration = iteration_end_time - iteration_start_time # time spent executing code
    if (iteration_duration < execution_period):
        time.sleep(execution_period - iteration_duration)



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
