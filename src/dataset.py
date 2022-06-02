import pandas as pd
import torch
from torch.utils.data import Dataset
from typing import Tuple

class CapacitanceDataset(Dataset):
    """Encapsulates a data set of capacitance values and labels."""

    def __init__(self, filename: str):
        pass

    def __len__(self) -> int:
        pass

    def __getitem__(self, idx: int) -> Tuple[torch.tensor, torch.tensor]:
        pass