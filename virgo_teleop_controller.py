#!/usr/bin/env python3
import serial
import gesture_recognition_api

class VirgoTeleopController:
    def __init__(self):
        # API for gesture recognition
        self._api = gesture_recognition_api.API()

        # Functions to execute
        # self.init_serial()
        self.set_up_glove()
        self.run_glove()

    def init_serial(self):
        self.ser = serial.Serial(
            port=
            "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A1024FPT-if00-port0",
            baudrate=115200

        )
        print("Serial open")
        self.ser.isOpen()

    def set_up_glove(self) -> None:
        self._api.setup()

    
    # def run_joystick(self):
    #     try:
    #         print('Press CTRL+C to quit')
    #         running = True
    #         hadEvent = False
    #         upDown = 0.0
    #         leftRight = 0.0
    #         driveLeft = 0
    #         driveRight = 0
 
    #         # Loop indefinitely
    #         while running:
    #             # Get the latest events from the system
    #             hadEvent = False
    #             events = pygame.event.get()
    #             # Handle each event individually
    #             for event in events:
    #                 if event.type == pygame.QUIT:
    #                     # User exit
    #                     running = False
    #                 elif event.type == pygame.JOYBUTTONDOWN:
    #                     # A button on the joystick just got pushed down
    #                     print('joystick: %d, button: %d' %(event.joy, event.button))
    #                     hadEvent = True

    #                 elif event.type == pygame.JOYAXISMOTION:
    #                     # A joystick has been moved
    #                     print('event.joy: %d, event.axis: %d' %(event.joy, event.axis))
    #                     hadEvent = True

    #                 if hadEvent:

    #                     LT_value = self.joystick.get_axis(self.LT)
    #                     if (LT_value == -1.0):
    #                         # Read axis positions (-1 to +1)
    #                         if self.axisUpDownInverted:
    #                             upDown = -self.joystick.get_axis(
    #                                 self.axisUpDown)
    #                         else:
    #                             upDown = self.joystick.get_axis(
    #                                 self.axisUpDown)
    #                         # print("upDown: ",upDown)
    #                         if self.axisLeftRightInverted:
    #                             leftRight = -self.joystick.get_axis(
    #                                 self.axisLeftRight)
    #                         else:
    #                             leftRight = self.joystick.get_axis(
    #                                 self.axisLeftRight)
    #                     else:
    #                         upDown = 0.0
    #                         leftRight = 0.0
    #                     (driveLeft, driveRight) = steering(upDown, leftRight)


    #             _driveLeft = int(driveLeft * 100 + 100).to_bytes(1, "big")
    #             _driveRight = int(driveRight * 100 + 100).to_bytes(1, "big")
    #             n = self.ser.write(bytes.fromhex('FF'))
    #             n = self.ser.write(_driveLeft)
    #             n = self.ser.write(_driveRight)

    #     except KeyboardInterrupt:
    #         self.ser.close()
    #         exit()

    def run_glove(self):
        """Gets the user input from the glove and outputs it to the serial."""

        try:
            print('Press CTRL+C to quit')
            driveLeft = 0
            driveRight = 0

            while True:

                gesture = self._api.read_gesture()
                inputs = {
                    "stop": (0, 0),
                    "forward": (1, 1),
                    "backward": (-1, -1),
                    "left": (1, -1),
                    "right": (-1, 1)
                }

                (driveLeft, driveRight) = inputs[gesture]
                print(inputs[gesture])

        except KeyboardInterrupt:
            print("Exiting...")
            self.ser.close()
            exit()

if __name__ == '__main__':
    VirgoTeleopController()