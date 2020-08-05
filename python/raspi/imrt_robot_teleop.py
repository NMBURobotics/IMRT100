import imrt_robot_serial
import imrt_xbox
import time


ROBOT_WIDTH = 0.40 # m

def main():
    vx_gain = 2
    wz_gain = 4

    controller = imrt_xbox.IMRTxbox()

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


    try:
        while not motor_serial.shutdown_now:
            but_a = controller.get_a()
            but_b = controller.get_b()
            but_x = controller.get_x()
            but_y = controller.get_y()

            ax_lx = controller.get_left_x()
            ax_ly = controller.get_left_y()
            ax_rx = controller.get_right_x()
            ax_ry = controller.get_right_y()

            # use pos.x, pos.y and pos.distance to determin vx and wz
            vx = vx_gain * ax_ly#* (-1,1)[bd.position.y > 0]
            wz = -wz_gain * ax_rx #* (1,-1)[bd.position.y > 0]
            print(vx, wz)

            # calculate motor commands
            v1 = (vx - ROBOT_WIDTH * wz / 2) * 200
            v2 = (vx + ROBOT_WIDTH * wz / 2) * 200


            print ("HEI")
            # send motor commands
            motor_serial.send_command(int(v1), int(v2))


            #print("a: {}, b: {}, x: {}, y: {}, lx: {:+.2f}, ly: {:+.2f}, rx: {:+.2f}, ry: {:+.2f}".format(but_a, but_b, but_x, but_y, ax_lx, ax_ly, ax_rx, ax_ry), end='\r')

            time.sleep(0.1)


    finally:
        controller.shutdown()
        print("Exiting program")


if __name__ == '__main__':
    main()

