# Stretchsense Gesture Recognition
This project aims to provide an API to take in sensor readings from a StretchSense device and determine the gesture/hand sign made.  

It comprises:
1. A data collection script for the collection of training data from the peripheral.
2. A training script to train a Machine Learning model to recognise gestures based on the sensor data from the device.
3. An API that allows the user to connect to a StretchSense device and get the recognised gesture as output on the command line.

The file paths to store the collected raw data and trained model, the hyperparameters for machine learning, and the list of gestures to be trained and recognised can be easily adapted to the user's needs by editing the `src/config.yaml` file.

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
* Raw data file path
* Trained model file path
* Hyperparameters including:
    * Number of epochs
    * Learning rate
    * Batch size
    * Learning capacity
* Number of sensors on the peripheral
* The list of gestures
* Number of repetitions and sets of data to be collected for each gesture

### Data Collector
1. Switch on the Stretchsense peripheral.
2. Run the data collector script with:
```
$ python3 data_collection/data_collector.py
```
3. Select the peripheral by entering its corresponding number in the command line.
4. Select which hand the glove is made for (i.e. right handed or left handed glove) by entering either `r` or `l` in the command line for right and left respectively. 
5. When prompted, make the gestures shown and **hold** them until the next one is shown.
6. The data file will be stored in the file path specified in `src/config.yaml`

## Credits
Andrew Lo Zhi Sheng 

[![Github Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/wrewsama)
[![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/andrewlozhisheng/)