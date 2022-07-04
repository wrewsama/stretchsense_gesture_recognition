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
        data_file_path = ""
        num_reps = 0
        num_sets = 0
        gestures = []
        num_sensors = 0
        num_gestures = 0
        learning_cap = 0
        batch_size = 0
        num_epochs = 0
        lr = 0
        self._model_path = ""

        with open("src/config.yaml") as config:
            configyaml = yaml.load(config, Loader=yaml.loader.FullLoader)
            data_file_path = f"data/{configyaml['filenames']['data']}.csv"
            self._model_path = f"trained_models/{configyaml['filenames']['trained_model']}.pth"
            num_reps = configyaml["general"]["num_reps"]
            num_sets = configyaml["general"]["num_sets"]
            gestures = configyaml["general"]["gestures"]
            num_gestures = len(gestures)
            num_sensors = configyaml["general"]["num_sensors"]
            learning_cap = configyaml["hyperparams"]["learning_capacity"]
            batch_size = configyaml["hyperparams"]["batch_size"]
            num_epochs = configyaml["hyperparams"]["num_epochs"]
            lr = configyaml["hyperparams"]["lr"]

        self._data_collector = data_collector.DataCollector(data_file_path,
                                                            num_reps,
                                                            num_sets,
                                                            gestures,
                                                            num_sensors)

        # # Instantiate model
        # model = feed_forward.FeedForwardModel(num_sensors,
        #                                       num_gestures,
        #                                       learning_cap)

        # # Choose optimiser function
        # optimiser_function = torch.optim.SGD

        # # Create the trainer object
        # self._trainer = train.Trainer(data_file_path,
        #                               batch_size,
        #                               num_epochs,
        #                               lr,
        #                               model,
        #                               optimiser_function)

        self._view = gui.View(self)

    def main(self):
        self._view.main()

    def update_gesture(self, gesture: str):
        """Updates the current gesture being trained."""

        self._view.curr_gesture.set(gesture)

if __name__ == "__main__":
    controller = Controller()
    controller.main()
    
        
    