import pandas as pd

df = pd.read_csv("data/example_dataset.csv")

rockdf = df[df["gesture_name"] == "rock"]
paperdf = df[df["gesture_name"] == "paper"]
scissorsdf = df[df["gesture_name"] == "scissors"]

print(rockdf.iloc[:, 2:9].mean())
print(paperdf.iloc[:, 2:9].mean())
print(scissorsdf.iloc[:, 2:9].mean())