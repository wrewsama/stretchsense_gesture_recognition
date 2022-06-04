from typing import Dict, List, Tuple
import torch

class LogisticRegressionModel(torch.nn.Module):
    """A logistic regression using one Linear Transformation.
    
    Args:
        num_sensors:
            The number of sensors to be read.
        num_gestures:
            The number of gestures to be trained.
    """
    def __init__(self,
                 num_sensors: int,
                 num_gestures: int):
        self.model = torch.nn.Linear(num_sensors, num_gestures)

    def forward(self, input: torch.tensor) -> torch.tensor:
        """Apply the model to transform the input data."""
        return self.model(input)

    def training_step(self,
                      batch: Tuple[torch.tensor, torch.tensor]
                     ) -> torch.tensor:
        """Calculate the loss."""
        pass

    def validation_step(self,
                        batch: Tuple[torch.tensor, torch.tensor]
                        ) -> Dict[str, torch.tensor]:
        """Calculate the loss and accuracy for a batch."""
        pass

    def validation_epoch_end(self,
                             outputs: List) -> Dict[str, int]:
        """Calculate the loss and accuracy for the whole validation set."""
        pass

    def epoch_end(self,
                  epoch: int,
                  result: Dict[str, int]) -> None:
        pass

    