"""Example that uses the gesture API for a game of rock paper scissors"""

"""
config parameters:
    filenames:
        data: example_dataset
        trained_model: example_model
    hyperparams:
        num_epochs: 500
        lr: 0.00001
        batch_size: 128
        learning_capacity: 32
    general: 
        num_sensors: 7
        gestures:
            - rock
            - paper
            - scissors
        num_reps: 500
        num_sets: 1
"""
import gesture_recognition_api
import random

def get_choice() -> str:
    """Gets the computer's choice of move.
    
    Returns:
        A randomly selected string representing the computer's chosen move.
    """

    return random.choice(["rock", "paper", "scissors"])

def process_moves(player_choice: str, opponent_choice: str) -> str:
    """Gets the result of the game.
    
    Takes in the player's and the computer's moves and returns a string
    containing the game's result, in accordance with the standard rules of
    rock paper scissors.

    Args:
        player_choice:
            A string representing the choice of move of the player.
        opponent_choice:
            A string representing the choice of move of the computer.

    Returns:
        A string representing whether the player wins, loses, or draws the
        game.
    """

    if player_choice == opponent_choice:
        # If the choices are the same, game is a draw
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
    """Script containing the main game loop."""

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
        # Get player's choice
        player_choice = api.read_gesture()
        print(f"You choose: {player_choice}") # Display choice

        # Get computer's choice
        opp_choice = get_choice()
        print(f"Computer chose: {opp_choice}") # Display choice

        # Get and display the game result
        print(process_moves(player_choice, opp_choice))

        # Check if user wants to stop
        if input("\nContinue? Y/N: ") in ["n", "N"]:
            # Exit the game loop
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()