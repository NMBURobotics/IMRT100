# This program will require you to set up the Raspberry for I2C communication,
# install some packages and download a python module. A nice guide can be found at:
# http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/
#
# use RPi_I2C_driver.py from the following site rather than from the link above
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

import RPi_I2C_driver
import time

my_lcd = RPi_I2C_driver.lcd()
my_lcd.lcd_display_string_pos("IMRT 100", 1, 4)
my_lcd.lcd_display_string_pos("Anvendt Robotikk", 2, 0)
print("Bye!")
            

