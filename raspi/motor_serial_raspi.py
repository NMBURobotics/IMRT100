import sys
import serial
import threading
import time

MSG_SIZE = 10


# Checksum algorithm
# This algorithm takes in a list of bytes and returns a two byte checksum.
# The checksum is calculated and included in the message on the transmitting side.
# On the receiving side, the receiver calculates the checksum and compare the reulting value to the one included in the message.
# If the values match, we trust that the data contained in the message is uncorrupted
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
# This thread will run concurrently with our main thread
# This particular thread's only job is to listen to incomming messages
# The readline() function is set to block until it gets a newline character
# By hvaing it in a separate thread, it will not block the main thread while waiting for incomming messages
def rxThread(serial_port) :

    while True :
        rx_msg = serial_port.readline()
        print(rx_msg, '\n')
      
    


if __name__ == '__main__' :

    if len(sys.argv) == 1 : 
        port_name = "/dev/ttyACM0"
    else :
        port_name = sys.argv[1]

    try :
        serial_port = serial.Serial(port_name, baudrate=115200, timeout=None)
    except :
        print ("Could not open port: " + port_name + ". Is your robot connected?\nExiting program")
        sys.exit(1)

    print("Connected to: ", port_name)

    # Create and start serial receive thread
    rx_thread = threading.Thread(target=rxThread, args=(serial_port,))
    rx_thread.start()


    while True :

        # Get commands
        cmd_1 = 400
        cmd_2 = 100

        
        # Here we create and populate the message we want to send to the motor controller
        # Our message will contain the following 10 bytes:
        # [header, cmd1_high, cmd1_low, cmd2_high, cmd2_low, not_used, not_used, checksum_high, checksum_low, newline]
        # Values that cannot fit into one byte are split into two bytes (xx_high, xx_low) using bitwise logic
        
        tx_msg = [0] * MSG_SIZE

        tx_msg[0]  = ord('c')               # msg header
        tx_msg[1]  = (cmd_1 >> 8) & 0xff    # command, motor 1 high
        tx_msg[2]  = (cmd_1) & 0xff         # command, motor 1 low
        tx_msg[3]  = (cmd_2 >> 8) & 0xff    # command, motor 2 high
        tx_msg[4]  = (cmd_2) & 0xff         # command, motor 2 low
        tx_msg[-1] = ord('\n')              # finish message with newline

        crc = crc16(tx_msg[0:-3])           # calculate checksum
        tx_msg[-3] = (crc >> 8) & 0xff      # checksum high
        tx_msg[-2] = (crc) & 0xff           # checksum low
        

        # Send message
        serial_port.write(tx_msg)


        # Wait for a bit
        time.sleep(0.1)

