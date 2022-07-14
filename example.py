import gesture_recognition_api

def main() -> None:
    """Main script."""

    # Instantiate the API
    api = gesture_recognition_api.API()

    try:
        # Set up the object
        api.setup()
    except gesture_recognition_api.NoPeripheralFoundError as npfe:
        # If no peripheral can be connected, quit
        return

    input("Press ENTER to start.\n")

    while True:
        # Read and print gesture
        gesture = api.read_gesture()
        print(f"Detected: {gesture}") # Display

        # Check if user wants to stop
        if input("\nContinue? Y/N: ") in ["n", "N"]:
            # Exit the game loop
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()