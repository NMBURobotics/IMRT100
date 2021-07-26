# This program will require you to set up the Raspberry for I2C communication,
# install some packages and download a python module. A nice guide can be found at:
# http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/
#
# use RPi_I2C_driver.py from the following site rather than from the link above # https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

import RPi_I2C_driver   
import time

my_lcd = RPi_I2C_driver.lcd()
message = ["Hello world!", "How are you?", "My name is..", "ScreenMcScrnface", "I am a LCD"]
animation = ["^", ">", "v", "<"]
anim_idx = 0;

try:
    while True:
        # Print headline on top row
        my_lcd.lcd_display_string_pos("IMRT 100", 1, 4)

        # Loop through lines in message
        for line in message:

            # Each line should display for 28 * 0.1 s = 2.8 s
            for i in range(28):

                # if index i is a valid index for character in line 
                if i < len(line):
                    my_lcd.lcd_display_string_pos(line[i], 2, i)

                # Update animation every second iteration
                if i%2 ==0:
                    my_lcd.lcd_display_string_pos(3*animation[anim_idx], 1, 0)
                    my_lcd.lcd_display_string_pos(3*animation[anim_idx], 1, 13)
                    anim_idx = (anim_idx + 1) % len(animation)

                # Sleep for 0.1 seconds
                time.sleep(0.1)

            # Clear second row by filling it with whitespace
            my_lcd.lcd_display_string_pos(16*" ", 2, 0)

except KeyboardInterrupt:
    print("Terminated by user")

finally:
    print("Bye!")
            

