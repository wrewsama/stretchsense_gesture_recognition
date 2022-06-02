"""Handler for StretchSense Peripherals using Bluetooth."""

from typing import List, Dict, Optional
import numpy as np
from bluepy import btle
from peripheral import stretchsense_delegate as ssd
from peripheral import stretchsense_peripheral as ssp
import yaml

class BluetoothHandler:
    """Handles connecting to a StretchSense device via Bluetooth Low Energy.
    
    Args:
        pkg_directory:
            A string representing the the filepath to this package.
    """

    def __init__(self, pkg_directory: str):
        self._pkg_directory: str = pkg_directory

        # Store known peripherals in a dict with addresses as keys
        # and names as values. For this project, there are no known peripherals
        self._known_peripherals: Dict = {}

    def _get_available_peripherals(self) -> List:
        """Gets a list of the available Stretchsense Peripherals."""

        # Create scanner
        scanner = btle.Scanner().withDelegate(
            ssd.StretchSenseDelegate())

        # Scan for devices for a maximum of 3 seconds.
        devices = scanner.scan(3)

        # Scan all available devices and return a list of available stretchsense devices
        available_peripherals = []
        for dev in devices:
            for (sdid, desc, val) in dev.getScanData():
                if val == 'StretchSense':
                    available_peripherals.append(dev.addr)
        return available_peripherals

    def _select_peripheral(self, 
                           available_peripherals: List) -> str:
        """Allow user to select a peripheral to connect to.
        
        Args:
            available_peripherals:
                The list of the addresses of the available StretchSense
                bluetooth devices.

        Returns:
            The address of the user-selected peripheral.
        """
        
        print('Select a glove to connect\n')

        # Display available peripherals
        for idx, addr in enumerate(available_peripherals):
            if addr in self._known_peripherals.keys(): # If the device is known
                print(f"{idx}. {addr}")
            else:
                print(f"{idx}. Unknown, addr: {addr}") # If device is unknown

        # Prompt user for selection
        selected = int(input("\n Select glove from 0 to " +
                                f"{len(available_peripherals) - 1}: "))

        # Return the address of the selected peripheral
        return available_peripherals[selected]
    
    def _get_glove(self, address: str) -> ssp.StretchSensePeripheral:
        """Returns a glove object corresponding to the given address."""

        if address in self._known_peripherals.keys(): # Peripheral is known
            # Return glove based on name
            if self._known_peripherals[address] == "left_glove":
                print("\n Left Glove detected.")
                return ssp.LeftStretchSenseGlove(address)
            elif self._known_peripherals[address] == "right_glove":
                print("\n Right Glove detected.")
                return ssp.RightStretchSenseGlove(address)

        else: # Peripheral is unknown
            # Prompt user for input and return appropriate glove
            side = input("\n Is this a right or left handed glove? R/L: ")
            if side in ["l", "left"]:
                return ssp.LeftStretchSenseGlove(address)
            elif side in ["r", "right"]:
                return ssp.RightStretchSenseGlove(address)
            else:
                # Prompt again if input is invalid
                print("\n Error: invalid input")
                return self._get_glove(address)

    def connect_peripheral(self) -> Optional[ssp.StretchSensePeripheral]:
        """Connect to a selected StretchSense Peripheral.
        
        Scans for available Bluetooth Low Energy devices, allows user to
        choose a Stretchsense Peripheral to connect to, sets the glove up, then
        returns it.

        Returns:
            A StretchSensePeripheral object or None.
        """

        # Get a list of available peripherals
        available_peripherals = self._get_available_peripherals()

        if available_peripherals: # If list is not empty
            # Get input from user
            addr = self._select_peripheral(available_peripherals)

            # Get the appropriate glove object
            glove = self._get_glove(addr)

            # Connect to glove
            print(f"\n connecting to addr: {addr}")
            glove.setup()

            # Return glove object
            return glove

        else: # If list is empty (i.e. no available peripherals)
            print(' No peripherals found.\n')

    