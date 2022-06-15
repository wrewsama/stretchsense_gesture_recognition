"""Script to get input from user and output the predicted gesture."""

import torch
from typing import List

import yaml
from src.models import feed_forward
from data_collection.peripheral import bluetooth_handler

class NoPeripheralFoundError(Exception):
    """Raised when there is no peripheral to connect to."""

    def __init__(self):
        super().__init__("No peripherals found")

class API:
    """API that gets input from user and outputs predicted gesture."""

    def setup(self) -> None:
        """Prepares for gesture recognition.
        
        Connects to peripheral and loads in gesture list and trained model.

        Raises:
            NoPeripheralFoundError when no peripherals can be found.
        """

        if self._connect_peripheral():
            self._load_model()
            self._load_gestures()
        else:
            raise NoPeripheralFoundError()

    def _connect_peripheral(self) -> bool:
        """Gets a Stretchsense peripheral for user input.
        
        Returns:
            True if peripheral is connected.
            False otherwise.
        """

        handler = bluetooth_handler.BluetoothHandler("")
        self._peripheral = handler.connect_peripheral()
        return self._peripheral is not None

    def _load_model(self) -> None:
        """Gets the trained model.
        
        Instantiate a specified model and load its parameters from a specified
        .pth file from the trained_models directory.
        """

        # Get params from config file
        num_sensors = 0
        num_gestures = 0
        learning_cap = 0
        modelpath = ""
        with open("src/config.yaml") as config:
            configyaml = yaml.load(config, Loader=yaml.loader.FullLoader)

            num_sensors = configyaml["general"]["num_sensors"]
            num_gestures = len(configyaml["general"]["gestures"])
            learning_cap = configyaml["hyperparams"]["learning_capacity"]
            modelpath = configyaml["filepaths"]["trained_model"]

        # Instantiate model
        model = feed_forward.FeedForwardModel(num_sensors,
                                            num_gestures,
                                            learning_cap)

        # Load in parameters from trained model
        model.load_state_dict(torch.load(modelpath))

        # Return the model
        self._model = model

    def _load_gestures(self) -> None:
        """Gets the list of gestures the model was trained with."""

        # Getting list from config file
        gestures = []
        with open("src/config.yaml") as config:
            configyaml = yaml.load(config, Loader=yaml.loader.FullLoader)
            gestures = configyaml["general"]["gestures"]

        self._gestures = gestures

    def read_gesture(self) -> str:
        # Get input data from the peripheral
        testdata = self._get_input()

        # Generate the prediction using the model
        output = self._model(torch.tensor(testdata))
        resultidx = torch.argmax(output).item()
        result = self._gestures[resultidx]
        
        # Display the prediction
        print(f"\nDetected gesture: {result}")

    def _get_input(self) -> List[int]:
        """Gets the input data from the connected peripheral.
        
        Args:
            peripheral:
                The Stretchsense peripheral whose sensor data needs to be read.

        Returns:
            A list of integers representing the sensor data.
        """

        # Clear old sensor readings
        for _ in range(300):
            self._peripheral.read_sensors()

        # Take new sensor readings until a non-nil reading is obtained
        data = None
        while data is None:
            data = self._peripheral.read_sensors()

        # Convert to list and return
        return data.tolist()

def main() -> None:
    """Main app script."""
    api = API()

    try:
        api.setup()
    except NoPeripheralFoundError as npfe:
        return

    # Repeat until user decides to stop
    flag = True
    while flag:
        api.read_gesture()

        # Checking if user wants to do another gesture
        print("\n Again? [Y/N]: ")
        if input() not in ["y", "Y", ""]:
            flag = False
            print("Exiting...")

if __name__ == "__main__":
    main()