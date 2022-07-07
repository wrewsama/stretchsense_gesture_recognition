"""The controller that links the data collector and trainer to the GUI."""
from regex import F
import yaml
import gui
from data_collection import data_collector
from typing import List
from src import train
from src.models import feed_forward
import torch

class Controller:
    def __init__(self):
         # Parameter setup
        self._collector: data_collector.DataCollector
        self._trainer: train.Trainer
        self._view = gui.View(self)

    def main(self):
        self._view.main()

    def load_peripheral_list(self) -> None:
        """Loads the peripheral list and returns whether there are 
        peripherals available.
        """

        self._load_data_collector()
        peripherals = self._collector.get_available_peripherals()

        if peripherals:
            # Display available peripherals
            for idx, addr in enumerate(peripherals):
                self._view.peripherals.insert(idx + 1, addr)
            return True
        else:
            # No available peripherals
            return False

    def _load_data_collector(self):
        # Parameter setup
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
        # Get user's selection from the view (GUI)
        selected = self._view.peripherals.curselection()

        # Return the address of the selected peripheral
        return self._view.peripherals.get(selected)

    def connect_to_peripheral(self) -> bool:
        return self._collector.connect()

    def update_text(self, text: str):
        """Updates the current gesture being trained."""

        self._view.curr_text.set(text)
        self._view.update_idletasks()

    def run_data_collector(self) -> None:
        self._collector.collect_data()

    def train(self) -> None:
        self._load_trainer()
        self._trainer.train()
        torch.save(self._model.state_dict(), self._model_path)

    def _load_trainer(self):
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
    
        
    