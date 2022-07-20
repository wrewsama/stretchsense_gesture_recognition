"""Allow user to set up the gesture recognition model with a GUI."""
import yaml
import gui
from data_collection import data_collector
from src import train
from src.models import feed_forward
import torch

class Controller:
    """Class to control the View(GUI).
    
    Enables the data collector, bluetooth handler, and the trainer to
    communicate with the GUI and vice versa. 
    """

    def __init__(self):
        # Parameter setup
        self._collector: data_collector.DataCollector
        self._trainer: train.Trainer

        # Instantiating the View(GUI)
        self._view = gui.View(self)

    def main(self):
        """The main application function."""

        # Turn on the GUI
        self._view.main()

    def load_peripheral_list(self) -> bool:
        """Loads the peripheral list and returns whether there are 
        peripherals available.

        Returns:
            True if there are available Bluetooth peripherals.
            False otherwise.
        """

        # Load the data collector with the current config parameters
        self._load_data_collector()

        # Get the list of available peripherals from the collector
        peripherals = self._collector.get_available_peripherals()

        if peripherals:
            # If there are available peripherals,
            # Display all available peripherals within the listbox in the GUI
            for idx, addr in enumerate(peripherals):
                self._view.peripherals.insert(idx + 1, addr)

            # Return True since peripherals are available
            return True
        else:
            # No available peripherals, hence False must be returned
            return False

    def _load_data_collector(self) -> None:
        """Loads the data collector with the current parameters in config.
        
        Retrieves the required parameters from the config file, then
        initialises a DataCollector instance using those parameters and store
        it in the self._collector field.
        """

        # Retrieve parameters
        data_file_path = ""
        num_reps = 0
        num_sets = 0
        gestures = []
        num_sensors = 0
        with open("src/config.yaml") as config:
            configyaml = yaml.load(config, Loader=yaml.loader.FullLoader)
            data_file_path = f"data/{configyaml['filenames']['data']}.csv"
            num_reps = configyaml["general"]["num_reps"]
            num_sets = configyaml["general"]["num_sets"]
            gestures = configyaml["general"]["gestures"]
            num_sensors = configyaml["general"]["num_sensors"]

        # Instantiate a data collector with the given parameters
        self._collector = data_collector.DataCollector(data_file_path,
                                                       num_reps,
                                                       num_sets,
                                                       gestures,
                                                       num_sensors,
                                                       self)

    def get_selection(self) -> str:
        """Gets the user input from the GUI.
        
        Gets the address of the peripheral that the user selected from the
        peripherals listbox in the GUI.

        Returns:
            String containing the address of the selected peripheral.
        """
        # Get user's selection from the view (GUI)
        selected = self._view.peripherals.curselection()

        # Return the address of the selected peripheral
        return self._view.peripherals.get(selected)

    def connect_to_peripheral(self) -> bool:
        """Connects to the peripheral by calling the datacollector's connect
        method.
        """

        return self._collector.connect()

    def update_text(self, text: str):
        """Updates the current gesture being trained."""

        self._view.curr_text.set(text)
        self._view.update_idletasks()

    def run_data_collector(self) -> None:
        """Calls collector's collect data method to begin data collection."""

        self._collector.collect_data()

    def train(self) -> None:
        """Loads, trains, and saves a model."""

        self._load_trainer()
        self._trainer.train()
        torch.save(self._model.state_dict(), self._model_path)

    def _load_trainer(self):
        """Loads a model and a trainer with the current parameters in config.
        
        Retrieves the required parameters from the config file, then
        initialises a FeedForwardModel and a Trainer instance using those
        parameters and stores it in the self._model and self._trainer fields
        respectively.
        """

        # Set up parameters
        num_sensors = 0
        num_gestures = 0
        learning_cap = 0
        data = ""
        batch_size = 0
        num_epochs = 0
        lr = 0
        self._model_path = ""
        with open("src/config.yaml") as config:
            configyaml = yaml.load(config, Loader=yaml.loader.FullLoader)

            # General parameters
            num_sensors = configyaml["general"]["num_sensors"]
            num_gestures = len(configyaml["general"]["gestures"])

            # Hyperparameters for machine learning
            learning_cap = configyaml["hyperparams"]["learning_capacity"]
            batch_size = configyaml["hyperparams"]["batch_size"]
            num_epochs = configyaml["hyperparams"]["num_epochs"]
            lr = configyaml["hyperparams"]["lr"]

            # File paths
            data = f"data/{configyaml['filenames']['data']}.csv"
            self._model_path = f"trained_models/{configyaml['filenames']['trained_model']}.pth"

        # Instantiate model
        self._model = feed_forward.FeedForwardModel(num_sensors,
                                            num_gestures,
                                            learning_cap)

        # Choose optimiser function
        optimiser_function = torch.optim.SGD

        # Create the trainer object
        self._trainer = train.Trainer(data,
                        batch_size,
                        num_epochs,
                        lr,
                        self._model,
                        optimiser_function)

if __name__ == "__main__":
    controller = Controller()
    controller.main()
    
        
    