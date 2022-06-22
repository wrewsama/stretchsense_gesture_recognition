# Stretchsense Gesture Recognition
This project aims to provide an API to take in sensor readings from a StretchSense device and determine the gesture/hand sign made.  

It comprises:
1. A data collection script for the collection of training data from the peripheral.
2. A training script to train a Machine Learning model to recognise gestures based on the sensor data from the device.
3. An API that allows the user to connect to a StretchSense device and get the recognised gesture.
4. A simple example script utilising the API to play a game of Rock Paper Scissors.

The file paths to store the collected raw data and trained model, the hyperparameters for machine learning, and the list of gestures to be trained and recognised can be easily adapted to the user's needs by editing the `src/config.yaml` file.

## Table of Contents
1. [Technologies Used](#technologies-used)
2. [Installation](#installation)
3. [Usage](#usage)
    * [Config File](#config-file)
    * [Data Collector](#data-collector)
    * [Trainer](#trainer)
    * [API](#api)
    * [Example use of API](#example---rock-paper-scissors)
4. [Models](#models)
    * [Simple Logistic Regression](#1-simple-logistic-regression)
    * [Feed Forward](#2-feed-forward-network-with-one-hidden-layer)
5. [Credits](#credits)

## Technologies Used
This project utilises the following technologies:

[BluePy](https://github.com/IanHarvey/bluepy) - For connecting to and collecting input from the peripherals.

[PyTorch](https://pytorch.org/) - For making and training machine learning models.

## Installation
1. Clone with:
```
# git clone https://github.com/wrewsama/stretchsense_gesture_recognition.git
```
2. Install dependencies with:
```
$ pip install -r requirements.txt
```

3. Optional: In order to use bluepy without sudo

Find the module directory by creating and running the following Python script:
```python
import bluepy
print(bluepy.__file__)
```

Go to the directory and run
```
$ sudo setcap 'cap_net_raw,cap_net_admin+eip' bluepy-helper
```

## Usage
An example use of the gesture recognition API to play a simple game of Rock Paper Scissors has been included in the `example.py` script. Configuration details, as well as instructions to train the model can be found in the docstring at the beginning of the script.

### Config File
Inside `src/config.yaml`, choose the:
* Raw data file name
* Trained model file name
* Hyperparameters including:
    * Number of epochs
    * Learning rate
    * Batch size
    * Learning capacity
* Number of sensors on the peripheral
* The list of gestures
* Number of repetitions and sets of data to be collected for each gesture

### Data Collector
1. Inside `src/config.yaml`, choose the:
    * Raw data file name
    * List of gestures
    * Number of repetitions and sets of data to be collected for each gesture
2. Switch on the Stretchsense peripheral.
3. Run the data collector script with:
```
$ python3 data_collection/data_collector.py
```
4. Select the peripheral by entering its corresponding number in the command line.
5. When prompted, make the gestures shown and **hold** them until the prompt states the gesture has been completed.
6. The data file will be stored in `data/<filename>.csv` where `filename` is the chosen raw data file name entered in `src/config.yaml`

### Trainer
1. Inside `src/config.yaml`, choose the:
    * Hyperparameters
    * File name of the raw data for training
    * File name of the file to store the trained model in
    * Number of sensors
2. Run the trainer script with:
```
$ python3 src/train.py
```
3. The accuracy and loss for every 10 epochs will be displayed in the command line and as a graph at the end of the training.
4. The trained model will be saved in `trained_models/<filename>.pth` where `filename` is the chosen trained model file name entered in `src/config.yaml`.

### API
The app can be imported with:
```python
import app
```

Set up with:
```python
api = app.API()
try:
    api.setup()
except NoPeripheralFoundError as npfe:
    print(npfe)    
```

Read gestures with:
```python
api.read_gesture()
```
This will return a string containing the name of the detected gesture.

### Example - Rock Paper Scissors
1. Inside `src/config.yaml`, use the following parameters:
```yaml
# Names of particular files to be created
filenames:
  data: example_dataset
  trained_model: example_model

# Hyperparameters for machine learning
hyperparams:
  num_epochs: 500
  lr: 0.00001
  batch_size: 128
  learning_capacity: 32

# General parameters
general: 
  num_sensors: 7
  gestures:
    - rock
    - paper
    - scissors
  num_reps: 500
  num_sets: 1
```
2. Run the [Data Collector](#data-collector)
3. Run the [Trainer](#trainer)
4. Run the example script using:
```
$ python3 example.py
```
5. Select the peripheral by entering its corresponding number in the command line.
6. Make your move and press the `ENTER` key
7. Your detected move, the computer opponent's move, and the game result will be printed out on the command line.
8. To quit, enter `n` into the command line, to continue, just press `ENTER`

## Models

Models tested with:
* Batch size of 128
* 500 epochs
* Learning rate of 1e-5
* Stochastic Gradient Descent optimiser

### 1. Simple Logistic Regression
![graph](https://i.ibb.co/bR73swV/Screenshot-from-2022-06-21-14-44-50.png")

Reaches 99% accuracy after approximately 200 epochs

### 2. Feed Forward Network With One Hidden Layer 
![graph](https://i.ibb.co/WBXPTPP/Screenshot-from-2022-06-21-14-45-05.png) 

Reaches 99% accuracy after about 30 epochs

## Credits
Andrew Lo Zhi Sheng 

[![Github Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/wrewsama)
[![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/andrewlozhisheng/)