import csv
import sys
import time
from typing import List, Tuple

import yaml

from .peripheral import bluetooth_handler
from .peripheral import stretchsense_peripheral as ssp


class DataCollector:
    """This class collects data from the Stretchsense Glove.
    
    Args:
        filepath:
            A string specifying the path to the file the collected data
            will be stored in.
        num_reps:
            Number of samples taken for 1 set of a particular gesture.
        num_sets:
            Number of sets of each gesture taken.
        gestures:
            A list of the names of the gestures to be trained.
        num_sensors:
            Number of sensors in the peripheral used for data collection.
        controller:
            The controller used to facilitate communication with the GUI.
    """

    def __init__(self,
                 filepath: str,
                 num_reps: int,
                 num_sets: int,
                 gestures: List,
                 num_sensors: int,
                 controller):

        # The handler used to connect to Stretchsense peripherals via Bluetooth
        self._handler: bluetooth_handler.BluetoothHandler

        # The peripheral used to collect sensor data
        self._peripheral: ssp.StretchSensePeripheral

        self._filepath: str = filepath
        self._num_reps: int = num_reps
        self._num_sets: int = num_sets
        self._gestures: List[str] = gestures
        self._num_sensors: int = num_sensors

        self._controller = controller

    def get_available_peripherals(self) -> List[str]:
        self._handler = bluetooth_handler.BluetoothHandlerWithGUI(self._controller)
        return self._handler.get_available_peripherals()

    def connect(self) -> bool:
        """Connects to a peripheral and sets up the instance fields."""

        self._peripheral = self._handler.connect_peripheral()

        return self._peripheral is not None

    def collect_data(self) -> None:
        """Collects and saves the required data."""
        
        # Setting up output lists
        inputs = []
        targets = []

        # Main data collection loop
        for _ in range(self._num_sets):
            # Repeat num_sets times
            for idx, gesture in enumerate(self._gestures):
                # For each gesture,
                # Display gesture name
                print(f"Current gesture: {gesture}")
                self._controller.update_text(gesture)
                time.sleep(1)

                # Clear up the old sensor data
                for _ in range(300):
                    self._peripheral.read_sensors()

                print("Recording now")

                # Collect data for given gesture
                rep_count = 0
                while rep_count < self._num_reps:
                    # For each rep,
                    # Read sensors
                    sensor_input = self._peripheral.read_sensors()

                    # Check if input is a valid rep
                    if sensor_input is None:
                        continue # If invalid, skip
                    
                    # Update targets
                    targets.append([idx, gesture])

                    # Update inputs as lists
                    inputs.append(sensor_input.tolist())

                    # Increment counter
                    rep_count += 1
                
                print("gesture completed")
                time.sleep(1)
        
        self._save_csv(inputs, targets)


    def _save_csv(self,
                    input_data: List[List[float]],
                    target_data: List[List[str]]) -> None:
        """Creates a csv file to store the collected data."""
        
        # Generate headers
        headers = ["gesture_index",
                   "gesture_name"]
        for i in range(1, self._num_sensors + 1):
            headers.append(f"sensor{i}")

        # Write to given file path
        with open(f"{self._filepath}", "w+") as data_file:
            # Instantiate csv writer
            csv_writer = csv.writer(data_file)

            # Write headers
            csv_writer.writerow(headers)

            # Write for each sample
            total_num_samples = self._num_reps * self._num_sets * len(self._gestures)
            for i in range(total_num_samples):
                # Each row comprises the index and name of the gesture, followed by the sensors
                row = [*target_data[i], *input_data[i]]
                csv_writer.writerow(row)

def main():
    """The main script for the data collection."""

    # # Parameter setup
    # data_file_path = ""
    # num_reps = 0
    # num_sets = 0
    # gestures = []
    # num_sensors = 0
    # with open("src/config.yaml") as config:
    #     configyaml = yaml.load(config, Loader=yaml.loader.FullLoader)
    #     data_file_path = f"data/{configyaml['filenames']['data']}.csv"
    #     num_reps = configyaml["general"]["num_reps"]
    #     num_sets = configyaml["general"]["num_sets"]
    #     gestures = configyaml["general"]["gestures"]
    #     num_sensors = configyaml["general"]["num_sensors"]

    # # Instantiate a data collector with the given parameters
    # collector = DataCollector(data_file_path,
    #                           num_reps,
    #                           num_sets,
    #                           gestures,
    #                           num_sensors)

    # # Run the collector
    # collector.run()

if __name__ == "__main__":
    main()