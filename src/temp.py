import yaml

with open("src/config.yaml") as f:
    x = yaml.load(f, Loader=yaml.loader.FullLoader)
    print(x["general"]["gestures"])