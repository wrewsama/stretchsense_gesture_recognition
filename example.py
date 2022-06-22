"""Example that uses the gesture API for a game of rock paper scissors"""

"""
Inside src/config.yaml:
    #  Names of particular files to be created
    filenames:
    data: example_dataset
    trained_model: example_model

    # Hyperparameters for machine learning
    hyperparams:
    num_epochs: 500
    lr: 0.00001
    batch_size: 128
    learning_capacity: 32

    # General parameters
    general: 
    num_sensors: 7
    gestures:
        - rock
        - paper
        - scissors
    num_reps: 500
    num_sets: 1

Then run data_collection/data_collector.py and src/train.py 
"""
import gesture_recognition_api
import random

def get_choice() -> str:
    return random.choice(["rock", "paper", "scissors"])

def process_moves(player_choice: str, opponent_choice: str) -> str:
    if player_choice == opponent_choice:
        return "Draw"
    elif player_choice == "rock":
        if opponent_choice == "paper":
            return "You Lose"
        else:
            return "You Win"
    elif player_choice == "paper":
        if opponent_choice == "scissors":
            return "You Lose"
        else:
            return "You Win"
    elif player_choice == "scissors":
        if opponent_choice == "rock":
            return "You Lose"
        else:
            return "You Win"

def main() -> None:
    # Instantiate the API
    api = gesture_recognition_api.API()

    try:
        # Set up the object
        api.setup()
    except gesture_recognition_api.NoPeripheralFoundError as npfe:
        # If no peripheral can be connected, quit
        return

    input("Press ENTER to start.\n")
    # Game loop
    while True:
        player_choice = api.read_gesture()
        print(f"You choose: {player_choice}")
        opp_choice = get_choice()
        print(f"Computer chose: {opp_choice}")

        print(process_moves(player_choice, opp_choice))

        if input("\nContinue? Y/N: ") in ["n", "N"]:
            break

if __name__ == "__main__":
    main()