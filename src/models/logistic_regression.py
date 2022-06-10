from typing import Dict, List, Tuple
import torch
import torch.nn.functional as F

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
        super().__init__()
        self.model = torch.nn.Linear(num_sensors, num_gestures)

    def forward(self, input: torch.tensor) -> torch.tensor:
        """Apply the model to transform the input data."""

        return self.model(input)

    def training_step(self,
                      batch: Tuple[torch.tensor, torch.tensor]
                     ) -> torch.tensor:
        """Calculate the loss.
        
        Takes in a batch of training data from the training data loader,
        generates a prediction using this model, then calculates and returns
        the cross entropy loss between the predictions and the corresponding
        labels.

        Args:
            batch:
                A batch of training data from a torch DataLoader object.

        Returns:
            A torch tensor containing the cross entropy loss.
        """

        # Split batch into input and label tensors
        sensors, labels = batch

        # Get the "probabilities" from the model
        output = self(sensors)

        # Return the cross entropy loss
        return F.cross_entropy(output, labels)

    def validation_step(self,
                        batch: Tuple[torch.tensor, torch.tensor]
                        ) -> Dict[str, torch.tensor]:
        """Calculate the loss and accuracy for a batch.
        
        Takes in a batch of validation data from the validation data loader,
        generates a prediction using this model, then calculates and returns
        both the cross entropy loss and the accuracy.

        Args:
            batch:
                A batch of validation data from a torch DataLoader object.

        Returns:
            A dictionary containing the loss and accuracy. The keys are
            "validation_loss" and "validation_accuracy".
        """

        # Split batch into input and label tensors
        sensors, labels = batch

        # Get the "probabilities" from the model
        output = self(sensors)

        # Get the cross entropy loss
        loss = F.cross_entropy(output, labels)

        # Get the accuracy
        accuracy = self._calc_accuracy(output, labels)

        # Return in the form of a dict
        return {"validation_loss": loss,
                "validation_accuracy": accuracy}

    def _calc_accuracy(self,
                       outputs: torch.tensor,
                       labels: torch.tensor) -> torch.tensor:
        """Helper method to calculate the accuracy of a batch of data.
        
        Args:
            outputs:
                A tensor containing a batch of predictions from the model.
            labels:
                A tensor containing the correct labels corresponding to the
                inputs corresponding to the predictions.

        Returns:
            A tensor containing the accuracy for this batch.
        """

        # Find the gesture with the highest "probability" for each input
        _, predictions = torch.max(outputs, dim=1)

        # Find the total number of correct predictions over the total
        # number of predictions
        return torch.tensor(torch.sum(predictions == labels).item()
                            / len(predictions))

    def validation_epoch_end(self,
                             outputs: List) -> Dict[str, int]:
        """Calculate the loss and accuracy for the whole validation set.
        
        Takes in a list of dictionaries, each containing the loss and accuracy
        for a particular batch, and compile them into a single dictionary to
        be returned.

        Args:
            outputs:
                List of dictionaries containing loss and accuracy for
                particular batch.
        
        Returns:
            Dictionary containing loss and accuracy for the whole epoch. Keys
            are "validation_loss" and "validation_accuracy"
        """
        
        # Consolidate losses
        batch_losses = [output["validation_loss"] for output in outputs]
        epoch_loss = torch.stack(batch_losses).mean()

        # Consolidate accuracies
        batch_accs = [output["validation_accuracy"] for output in outputs]
        epoch_acc = torch.stack(batch_accs).mean()

        return {"validation_loss": epoch_loss.item(),
                "validation_accuracy": epoch_acc.item()}

    def epoch_end(self,
                  epoch: int,
                  result: Dict[str, int]) -> None:
        """Displays the loss and accuracy for the epoch.
        
        Args:
            epoch:
                The current epoch number.
            result:
                A dictionary containing the loss and accuracy calculated from
                the validation set for this epoch.
        """
        
        val_loss = result["validation_loss"]
        val_acc = result["validation_accuracy"]
        print(f"Epoch [{epoch}], validation loss: {val_loss}, validation accuracy: {val_acc}")