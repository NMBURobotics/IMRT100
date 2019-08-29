#!/usr/bin/env python

import struct
import threading
import time

class IMRTxbox:

    def __init__(self, device="/dev/input/js0"):
        self._mux = threading.Lock()
        self._device = device
        self._deadzone = 0.2
        self._shutdown_thread = False
        self._buttons = [False] * 15
        self._axes = [0.0] * 8
        self._button_idx = {
            "A":       0,
            "B":       1,
            "X":       2,
            "Y":       3,
            "LB":      4,
            "RB":      5,
            "Back":    6,
            "Start":   7,
            "Xbox":    8,
            "Lstick":  9,
            "Rstick": 10,
            "Left":   11,
            "Right":  12,
            "Up":     13,
            "Down":   14
        }

        self._axes_idx = {
            "LX": 0,
            "LY": 1,
            "LT": 2,
            "RX": 3,
            "RY": 4,
            "RT": 5
        }

        self._device_listener = threading.Thread(target=self._listen_thread)
        self._device_listener.start()

  

    def _listen_thread(self):

        EVENT_SIZE = struct.calcsize("ihBB")

        things_are_ok = True
        while not self._shutdown_thread:
            try:

                file = open(self._device, "rb")
                things_are_ok = True
                print("Xbox controller connected!")

                reading = True
                while reading:
                    event = file.read(EVENT_SIZE)
                    (time_, but_value, but_type, but_num) = struct.unpack("ihBB", event)
                    #print("time", time_, "value", but_value, "type", but_type, "num", but_num)
                    if but_type == 1:
                        self._mux.acquire()
                        self._buttons[but_num] = not self._buttons[but_num]
                        self._mux.release()
                    elif but_type == 2:
                        but_value /= 32767.
                        if abs(but_value) < self._deadzone:
                            but_value = 0.
                        self._mux.acquire()
                        self._axes[but_num] = but_value
                        self._mux.release()
                        
                    self._mux.acquire()
                    if self._shutdown_thread:
                        reading= False
                    self._mux.release()
                    #time.sleep(0.01)
            
            except OSError:
                if things_are_ok:
                    print("Cannot find xbox controller. Is it on?")
                    things_are_ok = False

                

    
        file.close()




    def shutdown(self, blocking=True):
        self._shutdown_thread = True
        if blocking:
            self._device_listener.join()


    def getLeftX(self):
        self._mux.acquire()
        ret_value = self._axes[self._axes_idx["LX"]]
        self._mux.release()
        return ret_value

    def getLeftY(self):
        self._mux.acquire()
        ret_value = self._axes[self._axes_idx["LY"]]
        self._mux.release()
        return ret_value

    def getLeftTrigger(self):
        self._mux.acquire()
        ret_value = self._axes[self._axes_idx["LT"]]
        self._mux.release()
        return ret_value

    def getRightX(self):
        self._mux.acquire()
        ret_value = self._axes[self._axes_idx["RX"]]
        self._mux.release()
        return ret_value

    def getRightY(self):
        self._mux.acquire()
        ret_value = self._axes[self._axes_idx["RY"]]
        self._mux.release()
        return ret_value

    def getRightTrigger(self):
        self._mux.acquire()
        ret_value = self._axes[self._axes_idx["RT"]]
        self._mux.release()
        return ret_value



    def getA(self):
        self._mux.acquire()
        ret_value = self._buttons[self._button_idx["A"]]
        self._mux.release()
        return ret_value

    def getB(self):
        self._mux.acquire()
        ret_value = self._buttons[self._button_idx["B"]]
        self._mux.release()
        return ret_value

    def getX(self):
        self._mux.acquire()
        ret_value = self._buttons[self._button_idx["X"]]
        self._mux.release()
        return ret_value

    def getY(self):
        self._mux.acquire()
        ret_value = self._buttons[self._button_idx["Y"]]
        self._mux.release()
        return ret_value

    def getLeftBumper(self):
        self._mux.acquire()
        ret_value = self._buttons[self._button_idx["LB"]]
        self._mux.release()
        return ret_value

    def getRightBumper(self):
        self._mux.acquire()
        ret_value = self._buttons[self._button_idx["RB"]]
        self._mux.release()
        return ret_value

    def getBack(self):
        return self._buttons[self._button_idx["Back"]]

    def getStart(self):
        return self._buttons[self._button_idx["Start"]]

    def getXbox(self):
        return self._buttons[self._button_idx["Xbox"]]

    def getLeftStick(self):
        return self._buttons[self._button_idx["Lstick"]]

    def getRightStick(self):
        return self._buttons[self._button_idx["Rstick"]]

    def getLeft(self):
        return self._buttons[self._button_idx["Left"]]

    def getRight(self):
        return self._buttons[self._button_idx["Right"]]

    def getUp(self):
        return self._buttons[self._button_idx["Up"]]

    def getDown(self):
        return self._buttons[self._button_idx["Down"]]
