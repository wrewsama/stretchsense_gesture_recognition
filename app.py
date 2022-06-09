"""Script to get input from user and output the predicted gesture."""

import torch
from typing import List
from src.models import feed_forward
from data_collection.peripheral import bluetooth_handler

def connect_peripheral():
    """Gets a Stretchsense peripheral for user input."""

    handler = bluetooth_handler.BluetoothHandler("")
    return handler.connect_peripheral()

def get_input(peripheral) -> List[int]:

    for _ in range(500):
        peripheral.read_sensors()

    return peripheral.read_sensors().tolist()

def get_model() -> feed_forward.FeedForwardModel:
    """Gets the trained model."""

    model = feed_forward.FeedForwardModel(7, 3, 32)
    model.load_state_dict(torch.load("trained_models/example_model.pth"))
    return model

def get_gestures() -> List[str]:
    """Gets the list of gestures the model was trained with."""

    return ["rock",
            "paper",
            "scissors",]

def main() -> None:
    """The main script for the application."""

    peripheral = connect_peripheral()

    model = get_model()

    gestures = get_gestures()

    flag = True
    while flag:
        testdata = get_input(peripheral)

        if testdata is None:
            continue

        output = model(torch.tensor(testdata))
        resultidx = torch.argmax(output).item()
        result = gestures[resultidx]
        
        print(f"Detected gesture: {result}")
        print("\n Again? [Y/N]: ")
        if input() not in ["y", "Y"]:
            flag = False
            print("Exiting...")

if __name__ == "__main__":
    main()