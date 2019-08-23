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
    #Sensor bak
    dist_1 = motor_serial.get_dist_1()
    #Sensor venstre
    dist_2 = motor_serial.get_dist_2()
    #Sensor høyre
    dist_3 = motor_serial.get_dist_3()
    #Sensor foran
    dist_4 = motor_serial.get_dist_4()
    print("Bak: 1", dist_1, "   Venstre2", dist_2,  "  Høyre:3", dist_3, "   Foran:4", dist_4)

    

    # Calculate commands for each motor using sensor readings
    # In this simple example we will multiply each sensor reading
    # with a constant to obtain our commands
    gain = 1
    
    #Venstre
    speed_motor_1 = dist_3 * gain
    #Høyre
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
