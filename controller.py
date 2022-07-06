"""The controller that links the data collector and trainer to the GUI."""
from regex import F
import yaml
import gui
from data_collection import data_collector
from typing import List
# from src import train
# from src.models import feed_forward
# import torch
from time import sleep # FOR TESTING DELETE LATER

class Controller:
    def __init__(self):
         # Parameter setup
        self._collector: data_collector.DataCollector
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

if __name__ == "__main__":
    controller = Controller()
    controller.main()
    
        
    