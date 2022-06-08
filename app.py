import torch
from src.models import feed_forward

def main():
    model = feed_forward.FeedForwardModel(7, 3, 32)
    model.load_state_dict(torch.load("trained_models/example_model.pth"))
    print(model(torch.tensor([125.9,279.0,131.4,304.0,297.3,282.8,286.9])))

if __name__ == "__main__":
    main()