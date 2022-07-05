"""The controller that links the data collector and trainer to the GUI."""
import yaml
import gui
from data_collection import data_collector
# from src import train
# from src.models import feed_forward
# import torch
from time import sleep # FOR TESTING DELETE LATER

class Controller:
    def __init__(self):
         # Parameter setup
        self._data_collector: data_collector.DataCollector
        self._view = gui.View(self)

    def main(self):
        self._view.main()

    def load_data_collector(self):
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

    def update_text(self, text: str):
        """Updates the current gesture being trained."""

        self._view.curr_text.set(text)
        self._view.update_idletasks()

    def run_data_collector(self) -> None:
        self._collector.run()

if __name__ == "__main__":
    controller = Controller()
    controller.main()
    
        
    