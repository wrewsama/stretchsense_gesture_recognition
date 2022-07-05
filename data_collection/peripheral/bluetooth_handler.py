"""Handler for StretchSense Peripherals using Bluetooth."""

from typing import List, Dict, Optional
from bluepy import btle
from . import stretchsense_delegate as ssd
from . import stretchsense_peripheral as ssp

class BluetoothHandler:
    """Handles connecting to a StretchSense device via Bluetooth Low Energy."""

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
            print(f"{idx}. {addr}")

        # Prompt user for selection
        selected = int(input("\nSelect glove from 0 to " +
                                f"{len(available_peripherals) - 1}: "))

        # Return the address of the selected peripheral
        return available_peripherals[selected]
    
    def _get_glove(self, address: str) -> ssp.StretchSensePeripheral:
        """Returns a glove object corresponding to the given address."""

        return ssp.StretchSenseGlove(address)

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
            print(f"\nconnecting to addr: {addr}")
            glove.setup()
            print(f"connected to {addr}")

            # Return glove object
            return glove

        else: # If list is empty (i.e. no available peripherals)
            print(' No peripherals found.\n')

class BluetoothHandlerWithGUI:
    """Handles connecting to a StretchSense device and GUI."""
    
    def __init__(self, controller):
        self._controller = controller

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
            print(f"{idx}. {addr}")

        # Prompt user for selection
        selected = int(input("\nSelect glove from 0 to " +
                                f"{len(available_peripherals) - 1}: "))

        # Return the address of the selected peripheral
        return available_peripherals[selected]
    
    def _get_glove(self, address: str) -> ssp.StretchSensePeripheral:
        """Returns a glove object corresponding to the given address."""

        return ssp.StretchSenseGlove(address)

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
            glove = ssp.StretchSenseGlove(addr)

            # Connect to glove
            print(f"\nconnecting to addr: {addr}")
            glove.setup()
            print(f"connected to {addr}")

            # Return glove object
            return glove

        else: # If list is empty (i.e. no available peripherals)
            print(' No peripherals found.\n')
    