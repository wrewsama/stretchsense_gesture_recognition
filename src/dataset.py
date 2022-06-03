import pandas as pd
import torch
from torch.utils.data import Dataset
from typing import Tuple

class CapacitanceDataset(Dataset):
    """Encapsulates a data set of capacitance values and labels."""

    def __init__(self, filename: str):
        data_file = pd.read_csv(filename)
        labels = data_file.iloc[:, 0].values
        inputs = data_file.iloc[ :, 2:9].values

        self.inputs = torch.tensor(inputs, dtype=torch.float32)
        self.labels = torch.tensor(labels)

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> Tuple[torch.tensor, torch.tensor]:
        return self.inputs[idx], self.labels[idx]