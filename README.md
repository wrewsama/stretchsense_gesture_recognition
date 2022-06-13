# Stretchsense Gesture Recognition
This project aims to provide an API to take in sensor readings from a StretchSense device and determine the gesture/hand sign made.  

It comprises:
1. A data collection script for the collection of training data from the peripheral.
2. A training script to train a Machine Learning model to recognise gestures based on the sensor data from the device.
3. An API that allows the user to connect to a StretchSense device and get the recognised gesture as output on the command line.

The file paths to store the collected raw data and trained model, the hyperparameters for machine learning, and the list of gestures to be trained and recognised can be easily adapted to the user's needs by editing the `src/config.yaml` file.
