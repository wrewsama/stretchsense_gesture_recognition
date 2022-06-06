"""Script for training the desired model."""
import torch
from torch.utils.data import random_split, DataLoader
from typing import List, Dict
from models import logistic_regression
import dataset

class Trainer:
    """This class is responsible for training a selected model."""

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
        ds = dataset.CapacitanceDataset(data_file_path)
        train_ds_size = len(ds) // 5 * 4
        train_ds, val_ds = random_split(ds,
                                        [train_ds_size,
                                         len(ds) - train_ds_size])

        self._train_loader = DataLoader(train_ds, batch_size, shuffle=True)
        self._val_loader = DataLoader(val_ds, batch_size)

    def train(self) -> List:
        """Training and validation loop."""

        history = []

        for epoch in range(self._num_epochs):
            # Training
            for batch in self._train_loader:
                loss = self._model.training_step(batch)
                loss.backward()
                self._optimiser.step()
                self._optimiser.zero_grad()

            # Validation
            result = self._evaluate(self._model, self._val_loader)
            self._model.epoch_end(epoch, result)
            history.append(result)

        return history

    def _evaluate(self,
                  model: torch.nn.Module,
                  val_loader: DataLoader) -> Dict[str, int]:
        """Calculate the loss and accuracy of a given model."""

        outputs = [model.validation_step(batch) for batch in val_loader]
        return model.validation_epoch_end(outputs)

if __name__ == "__main__":
    data = "data/example_dataset.csv"
    model = logistic_regression.LogisticRegressionModel(7, 3)
    optimiser_function = torch.optim.SGD
    trainer = Trainer(data, 128, 50, 1e-6, model, optimiser_function)
    trainer.train()
