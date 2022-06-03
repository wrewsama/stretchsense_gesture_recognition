import csv
import time
from typing import List, Tuple

from peripheral import bluetooth_handler
from peripheral import stretchsense_peripheral as ssp

class DataCollector:
    """This class collects data from the Stretchsense Glove.
    
    Args:
        filename:
            A string specifying the name of the file the collected data
            will be stored in.
        num_reps:
            Number of samples taken for 1 set of a particular gesture.
        num_sets:
            Number of sets of each gesture taken.
        gestures:
            A list of the names of the gestures to be trained.
    """

    def __init__(self,
                 filename: str,
                 num_reps: int,
                 num_sets: int,
                 gestures: List):
        self._handler: bluetooth_handler.BluetoothHandler
        self._peripheral: ssp.StretchSensePeripheral

        self._filename: str = filename
        self._num_reps: int = num_reps
        self._num_sets: int = num_sets
        self._gestures: List[str] = gestures

    def run(self) -> None:
        """Handle data collection.
        
        Connects to a peripheral, gets the required data from it, and save
        it as a csv file.
        """

        # Connect to peripheral
        if self._connect():

            # Get required data
            inputs, targets = self._collect_data()

            # Save as csv
            self._save_csv(inputs, targets)
    
    def _connect(self) -> bool:
        """Connects to a peripheral and sets up the instance fields."""

        self._handler = bluetooth_handler.BluetoothHandler("")
        self._peripheral = self._handler.connect_peripheral()

        return self._peripheral is not None

    def _collect_data(self) -> Tuple[List[List[float]], List[str]]:
        """Collects the required data."""
        
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
                time.sleep(2)

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
        
        return inputs, targets


    def _save_csv(self,
                    input_data: List[List[float]],
                    target_data: List[List[str]]) -> None:
        """Creates a csv file to store the collected data."""
        
        headers = ["gesture_index",
                   "gesture_name",
                   "sensor1",
                   "sensor2",
                   "sensor3",
                   "sensor4",
                   "sensor5",
                   "sensor6",
                   "sensor7",
                   ]

        with open(f"data/{self._filename}.csv", "w+") as data_file:
            # Instantiate csv writer
            csv_writer = csv.writer(data_file)

            # Write headers
            csv_writer.writerow(headers)

            # Write for each sample
            total_num_samples = self._num_reps * self._num_sets * len(self._gestures)
            for i in range(total_num_samples):
                row = [*target_data[i], *input_data[i]]
                csv_writer.writerow(row)

def main():
    """The main script for the data collection."""

    # Parameter setup
    gestures = ["rock",
                "paper",
                "scissors",]
    collector = DataCollector("example_dataset", 300, 1, gestures)

    # Run the collector
    collector.run()

if __name__ == "__main__":
    main()