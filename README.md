# Stretchsense Gesture Recognition
This project aims to provide an API to take in sensor readings from a StretchSense device and determine the gesture/hand sign made.  

It comprises:
1. A data collection script for the collection of training data from the peripheral.
2. A training script to train a Machine Learning model to recognise gestures based on the sensor data from the device.
3. A Graphical User Interface facilitating both the data collection and model training processes.
4. An API that allows the user to connect to a StretchSense device and get the recognised gesture.
5. A simple example script utilising the API to read and print the detected gestures.
6. Another example script that uses the API to play a game of Rock Paper Scissors.

The file paths to store the collected raw data and trained model, the hyperparameters for machine learning, and the list of gestures to be trained and recognised can be easily adapted to the user's needs through the GUI provided in `setup.py`, or by editing the `src/config.yaml` file directly.

## Table of Contents
1. [Technologies Used](#technologies-used)
2. [Installation](#installation)
3. [Usage](#usage)
    * [Config File](#config-file)
    * [Setup](#setup)
    * [API](#api)
    * [Example 1](#example)
    * [Example 2](#example-2---rock-paper-scissors)
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
An example use of the gesture recognition API to play a simple game of Rock Paper Scissors has been included in the `example2.py` script. Configuration details, as well as instructions to train the model can be found in the docstring at the beginning of the script.

### Setup
1. Run the setup script with:
```
$ python3 setup.py
```
2. Select the [config parameters](#config-file).
3. Choose whether to:
  * `COLLECT` a new data set (go to step 4).
  * `TRAIN` a model using the data set located in data file path (go to step 8)
  * `SAVE & EXIT`
4. Select the address of the desired Stretchsense peripheral from the list box and click `CONNECT`.
5. Click on `COLLECT DATA` to begin the data collection process.
6. Follow the gestures displayed on the GUI.
7. Click on `TRAIN` to begin training the model.
8. Click on `EXIT` to exit

### Config File
Inside `src/config.yaml`, you can choose:
* filenames
  * data - The name of the raw data file both to store the data collected by the DataCollector and to be used by the Trainer to train the model.
  * trained_model - The name of the file storing the parameters of the model trained by the Trainer.
* hyperparams - for training the model
  * num_epochs - The number of epochs
  * lr - Learning rate
  * batch_size - size of each batch of data loaded by the dataloader
  * learning_capacity - size of the hidden layer
* general
  * num_sensors - Number of sensors on the peripheral
  * gestures - A list of gestures
  * num_sets - Number of sets of data to be collected for each gesture
  * num_reps - Number of repetitions per set of data

Or, this can be done through the GUI in `setup.py`

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

### Example
1. Complete the setup by [running `setup.py`](#setup).
2. Run the example using:
```
$ python3 example.py
```
3. Select the peripheral by entering its corresponding number in the command line.
4. Press the ENTER key. The detected gesture will be printed on the the command line.
5. Enter 'n' into the command line to exit.

### Example 2 - Rock Paper Scissors
1. Inside `src/config.yaml`, use the following parameters:
```yaml
filenames:
  data: example_dataset
  trained_model: example_model
hyperparams:
  num_epochs: 500
  lr: 0.00001
  batch_size: 128
  learning_capacity: 32
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
$ python3 example2.py
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