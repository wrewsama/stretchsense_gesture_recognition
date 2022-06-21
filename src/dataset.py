import pandas as pd
import torch
from torch.utils.data import Dataset
from typing import Tuple

class CapacitanceDataset(Dataset):
    """Encapsulates a data set of capacitance values and labels.
    
    Args:
        filepath:
            A String containing the name of the path to the raw data file.
    """

    def __init__(self, filepath: str):
        # Load in the raw data as a pandas DataFrame object
        data_file = pd.read_csv(filepath)

        # Split up the data into the target labels (i.e. the gesture indices)
        # and the inputs (i.e. the sensor data)
        labels = data_file.iloc[:, 0].values
        inputs = data_file.iloc[:, 2:9].values

        # Converting to torch tensors
        self.inputs = torch.tensor(inputs, dtype=torch.float32)
        self.labels = torch.tensor(labels)

    def __len__(self) -> int:
        """Returns the size of the data set."""

        return len(self.labels)

    def __getitem__(self, idx: int) -> Tuple[torch.tensor, torch.tensor]:
        """ Gets a data sample.

        Takes in an index and gets a corresponding tuple containing tensors,
        one with an input and another with the corresponding label. Called
        by the torch DataLoader.
        """

        return self.inputs[idx], self.labels[idx]