# Stretchsense Gesture Recognition
This project aims to provide an API to take in sensor readings from a StretchSense device and determine the gesture/hand sign made.  

It comprises:
1. A data collection script for the collection of training data from the peripheral.
2. A training script to train a Machine Learning model to recognise gestures based on the sensor data from the device.
3. An API that allows the user to connect to a StretchSense device and get the recognised gesture as output on the command line.

The file paths to store the collected raw data and trained model, the hyperparameters for machine learning, and the list of gestures to be trained and recognised can be easily adapted to the user's needs by editing the `src/config.yaml` file.

## Technologies Used


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

### App
1. Inside `src/config.yaml`, choose the:
    * Hyperparameters
    * File name of the trained model
2. Run the app script with:
```
$ python3 app.py
```
3. Select the peripheral by entering its corresponding number in the command line.
4. The current gesture will be printed in the command line.
5. To continue, input "y" in the command line. To exit, input "n"

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

## Credits
Andrew Lo Zhi Sheng 

[![Github Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/wrewsama)
[![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/andrewlozhisheng/)