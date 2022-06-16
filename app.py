"""Script to get input from user and output the predicted gesture."""

import torch
from typing import List

import yaml
from src.models import feed_forward
from data_collection.peripheral import bluetooth_handler

class NoPeripheralFoundError(Exception):
    """Raised when there is no peripheral to connect to."""

    def __init__(self):
        super().__init__()

class API:
    """API that gets input from user and outputs predicted gesture."""

    def setup(self) -> None:
        """Prepares for gesture recognition.
        
        Connects to peripheral and loads in gesture list and trained model.

        Raises:
            NoPeripheralFoundError when no peripherals can be found.
        """
        # Attempt to connect to peripheral
        if self._connect_peripheral():
            # If peripheral connected, 
            # Load the trained model
            self._load_model()

            # Load the list of gestures
            self._load_gestures()
        else:
            # If no peripheral connected, raise error
            raise NoPeripheralFoundError()

    def _connect_peripheral(self) -> bool:
        """Gets a Stretchsense peripheral for user input.
        
        Returns:
            True if peripheral is connected.
            False otherwise.
        """

        # Create new handler
        handler = bluetooth_handler.BluetoothHandler()

        # Connect peripheral
        self._peripheral = handler.connect_peripheral()

        # Return whether there is a connected peripheral
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
            modelpath = f"trained_models/{configyaml['filenames']['trained_model']}.pth"

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

        # Updating gestures field
        self._gestures = gestures

    def read_gesture(self) -> str:
        # Get input data from the peripheral
        testdata = self._get_input()

        # Generate the prediction using the model
        output = self._model(torch.tensor(testdata))
        resultidx = torch.argmax(output).item()
        result = self._gestures[resultidx]
        
        # Return the prediction
        return result

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

    # Instantiate the api object
    api = API()

    try:
        # Set up the object
        api.setup()
    except NoPeripheralFoundError as npfe:
        # If no peripheral can be connected, quit
        return

    # Repeat until user decides to stop
    flag = True
    while flag:
        # Read and print gesture
        print(api.read_gesture())

        # Checking if user wants to do another gesture
        print("\n Again? [Y/N]: ")
        if input() not in ["y", "Y", ""]:
            flag = False
            print("Exiting...")

if __name__ == "__main__":
    main()