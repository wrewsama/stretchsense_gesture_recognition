#!/usr/bin/env python3
from threading import Thread
import multiprocessing as mp
import serial
import gesture_recognition_api

class VirgoTeleopController:
    def __init__(self):
        # API for gesture recognition
        self._api = gesture_recognition_api.API()

        # Container queue to store the current direction
        self._q = mp.Queue(1)

        # Functions to execute
        self.init_serial()
        self.set_up_glove()

        # initialise processes
        glove_reader = Thread(target=self.get_gesture)
        direction_publisher = Thread(target=self.run_glove)

        # Begin the processes
        glove_reader.start()
        direction_publisher.start()

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

    def run_glove(self):
        """Gets the user input from the glove and outputs it to the serial."""

        try:
            print('Press CTRL+C to quit')

            curr_direction = (0, 0)
            while True:
                if not self._q.empty():
                    # get the updated direction
                    curr_direction = self._q.get()         

                # Publish
                print(curr_direction) # will be replaced by some function to publish to serial
                left = (100 * curr_direction[0] + 100).to_bytes(1, "big")
                right = (100 * curr_direction[1] + 100).to_bytes(1, "big")

                self.ser.write(bytes.fromhex('FF'))
                self.ser.write(left)
                self.ser.write(right)

        except KeyboardInterrupt:
            print("Exiting publisher...")
            self.ser.close()
            exit()

    def get_gesture(self):
        """Reads the user's gesture."""

        try:
            while True:
                gesture = self._api.read_gesture()
                
                self.update_direction(gesture)

        except KeyboardInterrupt:
            print("Exiting reader...")

    def update_direction(self, gesture: str):
        """Updates queue with the current direction.
        
        Takes in a gesture and pushes a tuple
        """

        inputs = {
            "stop": (0, 0),
            "forward": (1, 1),
            "backward": (-1, -1),
            "left": (1, -1),
            "right": (-1, 1)
        }

        self._q.put(inputs[gesture])

if __name__ == '__main__':
    VirgoTeleopController()