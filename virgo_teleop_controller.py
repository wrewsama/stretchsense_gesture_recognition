#!/usr/bin/env python3

from pickle import TRUE
import time
import os
import sys
import pygame
import serial

import math


def steering(x, y):
    left, right = x - y, x + y

    # clamp to -1/+1
    left = max(-1, min(left, 1))
    right = max(-1, min(right, 1))

    return left, right

class VirgoTeleopController:
    def __init__(self):
        # Settings for the joystick
        self.axisUpDown = 4  # Joystick axis to read for up / down position
        self.axisUpDownInverted = True  # Set this to True if up and down appear to be swapped
        self.axisLeftRight = 0  # Joystick axis to read for left / right position
        self.axisLeftRightInverted = False  # Set this to True if left and right appear to be swapped
        self.buttonSlow = 8  # Joystick button number for driving slowly whilst held (L2)
        self.slowFactor = 0.5  # Speed to slow to when the drive slowly button is held, e.g. 0.5 would be half speed
        self.buttonFastTurn = 9  # Joystick button number for turning fast (R2)
        self.interval = 0.2  # Time between updates in seconds, smaller responds faster but uses more processor time
        self.joystick = None
        self.moveForward = 0.0
        self.moveSideways = 0.0
        self.LT = 2
        self.stopButtonpressed = False
        self.buffer = ""
        #Functions to execute
        self.init_serial()
        self.wait_for_joystick()
        self.run_joystick()

    def init_serial(self):
        self.ser = serial.Serial(
            port=
            "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A1024FPT-if00-port0",
            baudrate=115200

        )
        print("Serial open")
        self.ser.isOpen()

    def run_joystick(self):
        try:
            print('Press CTRL+C to quit')
            running = True
            hadEvent = False
            stopButtonpressed = False
            upDown = 0.0
            leftRight = 0.0
            driveLeft = 0
            driveRight = 0
 
            # Loop indefinitely
            while running:
                # Get the latest events from the system
                hadEvent = False
                events = pygame.event.get()
                # Handle each event individually
                for event in events:
                    if event.type == pygame.QUIT:
                        # User exit
                        running = False
                    elif event.type == pygame.JOYBUTTONDOWN:
                        # A button on the joystick just got pushed down
                        print('joystick: %d, button: %d' %(event.joy, event.button))
                        hadEvent = True

                    elif event.type == pygame.JOYAXISMOTION:
                        # A joystick has been moved
                        print('event.joy: %d, event.axis: %d' %(event.joy, event.axis))
                        hadEvent = True

                    if hadEvent:

                        LT_value = self.joystick.get_axis(self.LT)
                        if (LT_value == -1.0):
                            # Read axis positions (-1 to +1)
                            if self.axisUpDownInverted:
                                upDown = -self.joystick.get_axis(
                                    self.axisUpDown)
                            else:
                                upDown = self.joystick.get_axis(
                                    self.axisUpDown)
                            # print("upDown: ",upDown)
                            if self.axisLeftRightInverted:
                                leftRight = -self.joystick.get_axis(
                                    self.axisLeftRight)
                            else:
                                leftRight = self.joystick.get_axis(
                                    self.axisLeftRight)
                        else:
                            upDown = 0.0
                            leftRight = 0.0
                        (driveLeft, driveRight) = steering(upDown, leftRight)


                _driveLeft = int(driveLeft * 100 + 100).to_bytes(1, "big")
                _driveRight = int(driveRight * 100 + 100).to_bytes(1, "big")
                n = self.ser.write(bytes.fromhex('FF'))
                n = self.ser.write(_driveLeft)
                n = self.ser.write(_driveRight)

        except KeyboardInterrupt:
            self.ser.close()
            exit()


if __name__ == '__main__':
    VirgoTeleopController()