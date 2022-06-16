"""Script for training the desired model."""
import torch
from torch.utils.data import random_split, DataLoader
from typing import List, Dict

import yaml
from models import feed_forward
import dataset
import matplotlib.pyplot as plt

class Trainer:
    """This class is responsible for training a selected model.
    
    Args:
        data_file_path:
            A string containing the path to the raw data csv file.
        batch_size:
            The size of each batch of data put into the dataloader.
        num_epochs:
            The number of epochs to train the model for.
        lr:
            The learning rate for the model.
        model:
            The model object being trained.
        optimiser_funct:
            The class of the optimiser used to adjust the model's parameters.
    """

    def __init__(self,
                 data_file_path: str,
                 batch_size: int,
                 num_epochs: int,
                 lr: int,
                 model: torch.nn.Module,
                 optimiser_funct: torch.optim.Optimizer):

        self._num_epochs = num_epochs
        self._lr = lr
        self._model = model
        self._optimiser = optimiser_funct(model.parameters(), lr)

        # Get dataset from the raw csv data
        ds = dataset.CapacitanceDataset(data_file_path)

        # Split the data set into training and validation
        train_ds_size = len(ds) // 5 * 4
        train_ds, val_ds = random_split(ds,
                                        [train_ds_size,
                                         len(ds) - train_ds_size])

        self._train_loader = DataLoader(train_ds, batch_size, shuffle=True)
        self._val_loader = DataLoader(val_ds, batch_size)

    def train(self) -> List[Dict[str, int]]:
        """Training and validation loop.
        
        Returns:
            List containing dictionaries that keep track of the loss and
            accuracy for every epoch.
        """

        # List used to keep track of the loss and accuracy each epoch.
        history = []

        for epoch in range(self._num_epochs):
            # Training
            for batch in self._train_loader:
                loss = self._model.training_step(batch)
                loss.backward()
                self._optimiser.step()
                self._optimiser.zero_grad()

            # Validation (every 10 epochs)
            if epoch % 10 == 0:
                # Get loss and accuracy for the whole epoch
                result = self._evaluate(self._model, self._val_loader)

                # Print the results
                self._model.epoch_end(epoch, result)

                # Add it to history
                history.append(result)

        return history

    def _evaluate(self,
                  model: torch.nn.Module,
                  val_loader: DataLoader) -> Dict[str, int]:
        """Calculate the loss and accuracy of a given model.
        
        Args:
            model:
                The model to be evaluated.
            val_loader:
                A dataloader containing the validation dataset.

        Returns:
            A dictionary where the keys are either validation_loss or
            validation_accuracy and the values are their corresponding integer
            values.
        """

        # Get a list of all the losses and accuracies for each batch
        outputs = [model.validation_step(batch) for batch in val_loader]

        # Consolidate and return
        return model.validation_epoch_end(outputs)

    def visualise_loss(self, history: List) -> None:
        """Plots a graph of the loss over num of epochs."""

        losses = [x["validation_loss"] for x in history]
        plt.plot(losses, "-x")
        plt.xlabel("epoch")
        plt.ylabel("loss")
        plt.title("Loss vs Number of Epochs")
        plt.show()

    def visualise_acc(self, history: List) -> None:
        """Plots a graph of the accuracies over num of epochs."""

        losses = [x["validation_accuracy"] for x in history]
        plt.plot(losses, "-x")
        plt.xlabel("epoch")
        plt.ylabel("acc")
        plt.title("Accuracy vs Number of Epochs")
        plt.show()

def main() -> None:
    # Set up parameters
    num_sensors = 0
    num_gestures = 0
    learning_cap = 0
    data = ""
    batch_size = 0
    num_epochs = 0
    lr = 0
    model_path = ""
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
        data = configyaml["filepaths"]["data"]
        model_path = configyaml["filepaths"]["trained_model"]

    # Instantiate model
    model = feed_forward.FeedForwardModel(num_sensors,
                                          num_gestures,
                                          learning_cap)

    # Choose optimiser function
    optimiser_function = torch.optim.SGD

    # Create the trainer object
    trainer = Trainer(data,
                      batch_size,
                      num_epochs,
                      lr,
                      model,
                      optimiser_function)

    # Train the model
    history = trainer.train()

    # Check the accuracy graph
    trainer.visualise_acc(history)

    # Save the model's parameters
    torch.save(model.state_dict(), model_path)

if __name__ == "__main__":
    main()
    