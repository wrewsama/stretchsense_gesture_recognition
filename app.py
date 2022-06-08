import torch
from src.models import feed_forward

def main():
    model = feed_forward.FeedForwardModel(7, 3, 32)
    model.load_state_dict(torch.load("trained_models/example_model.pth"))

    gestures = ["rock",
                "paper",
                "scissors",]

    testdata = [125.9,279.0,131.4,304.0,297.3,282.8,286.9]
    output = model(torch.tensor(testdata))
    resultidx = torch.argmax(output).item()
    result = gestures[resultidx]
    
    print(result)

if __name__ == "__main__":
    main()