"""Script to get input from user and output the predicted gesture."""

import torch
from typing import List
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

    # Instantiate model
    model = feed_forward.FeedForwardModel(7, 3, 32)

    # Load in parameters from trained model
    model.load_state_dict(torch.load("trained_models/example_model.pth"))

    # Return the model
    return model

def get_gestures() -> List[str]:
    """Gets the list of gestures the model was trained with."""

    return ["rock",
            "paper",
            "scissors",]

def main() -> None:
    """The main script for the application."""

    # Connect to the peripheral
    peripheral = connect_peripheral()

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