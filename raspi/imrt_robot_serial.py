# NMBU Robotics 2019
# Author: Lars Grimstad


import sys
import serial
import threading
import time
import signal



# Class for communicating with the NMBU IMRT100 robot
class IMRTRobotSerial :

    MSG_SIZE = 10

    # Constructor
    def __init__(self):

        print("NMBU Robotics imrt100 motor serial")
        
        # Create an event for signaling threads when its time terminate the program
        self.run_event_ = threading.Event()
        self.run_event_.set()

        self.shutdown_now = False
        signal.signal(signal.SIGINT, self.shutdownSignal)
        

        # Thread for receiving data through serial
        self.rx_thread_ = threading.Thread(target=self.rxThread)



        
    # Method for opening serial port
    def connect(self, port_name="/dev/ttyACM0"):
        try :
            self.serial_port_ = serial.Serial(port_name, baudrate=115200, timeout=3)
        except :
            print ("Could not open port: " + port_name + ". Is your robot connected?")
            return False

        print("Connected to: ", port_name)
        return True



    
    # Method for starting serial receive thread
    def run(self):
        self.rx_thread_.start()


    def shutdownSignal(self, signum, frame):
        print("Shutdown signal received")
        self.shutdown_now = True
        self.shutdown()


    # Method for gracefully shutting down serial receive thread
    def shutdown(self, blocking=True):
        self.run_event_.clear()
        if blocking:
            self.rx_thread_.join()

        
        

    # Checksum algorithm
    # This algorithm takes in a list of bytes and returns a two byte checksum.
    # The checksum is calculated and included in the message on the transmitting side.
    # On the receiving side, the receiver calculates the checksum and compare the reulting value to the one included in the message.
    # If the values match, we trust that the data contained in the message is uncorrupted
    @staticmethod
    def crc16(data_list) :
        crc = 0x0000;
        POLY = 0x8408
      

        if len(data_list) == 0 :
            return (~crc)

        for byte in data_list :
            byte = 0xff & byte
            for i in range(8) :
                if ((crc & 0x0001) ^ (byte & 0x0001)) :
                    crc = (crc >> 1) ^ POLY
                else :
                    crc = crc >> 1
                byte = byte >> 1
        
        return (crc)




    # Thread for receiving serial messages
    # This thread will run concurrently with other threads
    # This particular thread's only job is to listen to incomming messages
    # The readline() function is set to block until it gets a newline character
    # By hvaing it in a separate thread, it will not block other threads while waiting for incomming messages
    def rxThread(self) :

        while self.run_event_.is_set() :
            rx_msg = self.serial_port_.readline()
            if(len(rx_msg) > 0) :
                print(rx_msg, '\n')

        print("Serial receive thread has finished")




    # Method for transmitting commands through serial
    def sendCommand(self, cmd_1, cmd_2) :
        
        # Here we create and populate the message we want to send to the motor controller
        # Our message will contain the following 10 bytes:
        # [header, cmd1_high, cmd1_low, cmd2_high, cmd2_low, not_used, not_used, checksum_high, checksum_low, newline]
        # Values that cannot fit into one byte are split into two bytes (xx_high, xx_low) using bitwise logic
        
        tx_msg = [0] * self.MSG_SIZE

        tx_msg[0]  = ord('c')               # msg header
        tx_msg[1]  = (cmd_1 >> 8) & 0xff    # command, motor 1 high
        tx_msg[2]  = (cmd_1) & 0xff         # command, motor 1 low
        tx_msg[3]  = (cmd_2 >> 8) & 0xff    # command, motor 2 high
        tx_msg[4]  = (cmd_2) & 0xff         # command, motor 2 low
        tx_msg[-1] = ord('\n')              # finish message with newline

        crc = self.crc16(tx_msg[0:-3])      # calculate checksum
        tx_msg[-3] = (crc >> 8) & 0xff      # checksum high
        tx_msg[-2] = (crc) & 0xff           # checksum low

        
        # Send message
        self.serial_port_.write(tx_msg)


          



def main(argv) :

    # Example program
    print("Example program")
    if len(argv) == 1 : 
        port_name = "/dev/ttyACM0"
    else :
        port_name = argv[1]

    # Create motor serial object
    motor_serial = IMRTRobotSerial()

    # Open serial port, exit if serial port can't be opened
    connected = motor_serial.connect(port_name)
    if not connected:
        print("Exiting program")
        sys.exit()
        
    # Spin receive thread
    motor_serial.run()


    # Now we will send some motor commands until the program is terminated by the user
    speed = 0
    try :
        while True :
            speed = (speed + 10) % 400
            motor_serial.sendCommand(speed, 400-speed)
            time.sleep(0.1)

    except KeyboardInterrupt :
        print("Shutting down threads")


    # Exit
    motor_serial.shutdown()
    print("Exiting program")




if __name__ == '__main__' :
    main(sys.argv)

 

