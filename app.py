"""Script to get input from user and output the predicted gesture."""

import torch
from typing import List

import yaml
from src.models import feed_forward
from data_collection.peripheral import bluetooth_handler

def connect_peripheral() -> None:
    """Gets a Stretchsense peripheral for user input."""

    handler = bluetooth_handler.BluetoothHandler("")
    return handler.connect_peripheral()

def get_input(peripheral) -> List[int]:
    """Gets the input data from a given peripheral.
    
    Args:
        peripheral:
            The Stretchsense peripheral whose sensor data needs to be read.

    Returns:
        A list of integers representing the sensor data.
    """

    # Clear old sensor readings
    for _ in range(300):
        peripheral.read_sensors()

    # Take new sensor readings until a non-nil reading is obtained
    data = None
    while data is None:
        data = peripheral.read_sensors()

    # Convert to list and return
    return data.tolist()

def get_model() -> feed_forward.FeedForwardModel:
    """Gets the trained model.
    
    Instantiate a specified model and load its parameters from a specified
    .pth file from the trained_models directory. 

    Returns:
        An instance of a trained model.
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
    return model

def get_gestures() -> List[str]:
    """Gets the list of gestures the model was trained with."""

    # Getting list from config file
    gestures = []
    with open("src/config.yaml") as config:
        configyaml = yaml.load(config, Loader=yaml.loader.FullLoader)
        gestures = configyaml["general"]["gestures"]

    return gestures

def main() -> None:
    """The main script for the application."""

    # Connect to the peripheral
    peripheral = connect_peripheral()

    # Check if peripheral is connected
    if peripheral is None:
        return

    # Get a trained model for predictions
    model = get_model()

    # Get the list of gestures that the model was trained with
    gestures = get_gestures()

    # Repeat until user decides to stop
    flag = True
    while flag:
        # Get input data from the peripheral
        testdata = get_input(peripheral)

        # Generate the prediction using the model
        output = model(torch.tensor(testdata))
        resultidx = torch.argmax(output).item()
        result = gestures[resultidx]
        
        # Display the prediction
        print(f"\nDetected gesture: {result}")

        # Checking if user wants to do another gesture
        print("\n Again? [Y/N]: ")
        if input() not in ["y", "Y", ""]:
            flag = False
            print("Exiting...")

if __name__ == "__main__":
    main()