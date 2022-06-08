from typing import Dict, List, Tuple
import torch
import torch.nn.functional as F

class FeedForwardModel(torch.nn.Module):
    """A feed forward network with 1 hidden layer.
    
    Args:
        num_sensors:
            The number of sensors to be read.
        num_gestures:
            The number of gestures to be trained.
        learning_capacity:
            The size of the hidden layer.
    """
    def __init__(self,
                 num_sensors: int,
                 num_gestures: int,
                 learning_capacity: int):
        super().__init__()
        self.model = torch.nn.Sequential(
            torch.nn.Linear(num_sensors, learning_capacity),
            torch.nn.ReLU(),
            torch.nn.Linear(learning_capacity, num_gestures)
        )

    def forward(self, input_: torch.tensor) -> torch.tensor:
        """Apply the model to transform the input data."""
        return self.model(input_)

    def training_step(self,
                      batch: Tuple[torch.tensor, torch.tensor]
                     ) -> torch.tensor:
        """Calculate the loss."""

        sensors, labels = batch
        output = self(sensors)
        return F.cross_entropy(output, labels)

    def validation_step(self,
                        batch: Tuple[torch.tensor, torch.tensor]
                        ) -> Dict[str, torch.tensor]:
        """Calculate the loss and accuracy for a batch."""

        sensors, labels = batch
        output = self(sensors)
        loss = F.cross_entropy(output, labels)
        accuracy = self._calc_accuracy(output, labels)
        return {"validation_loss": loss,
                "validation_accuracy": accuracy}

    def _calc_accuracy(self,
                       outputs: torch.tensor,
                       labels: torch.tensor) -> torch.tensor:
        """Helper method to calculate the accuracy of a batch of data."""

        _, predictions = torch.max(outputs, dim=1)
        return torch.tensor(torch.sum(predictions == labels).item()
                            / len(predictions))

    def validation_epoch_end(self,
                             outputs: List) -> Dict[str, int]:
        """Calculate the loss and accuracy for the whole validation set."""
        
        batch_losses = [output["validation_loss"] for output in outputs]
        epoch_loss = torch.stack(batch_losses).mean()

        batch_accs = [output["validation_accuracy"] for output in outputs]
        epoch_acc = torch.stack(batch_accs).mean()

        return {"validation_loss": epoch_loss.item(),
                "validation_accuracy": epoch_acc.item()}

    def epoch_end(self,
                  epoch: int,
                  result: Dict[str, int]) -> None:

        val_loss = result["validation_loss"]
        val_acc = result["validation_accuracy"]
        print(f"Epoch [{epoch}], validation loss: {val_loss}, validation accuracy: {val_acc}")