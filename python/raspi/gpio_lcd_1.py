# This program will require you to set up the Raspberry for I2C communication,
# install some packages and download a python module. A nice guide can be found at:
# http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/

import I2C_LCD_driver
import time

my_lcd = I2C_LCD_driver.lcd()
my_lcd.lcd_display_string("IMRT 100", 1, 4)
my_lcd.lcd_display_string("Anvendt Robotikk", 2, 0)
print("Bye!")
            

