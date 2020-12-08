#!/usr/bin/env python3
import os
from os import environ
import sys
import time
import subprocess
import datetime
from cv.locator import DroneLocator
import matplotlib.pyplot as plt
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import datasets, layers, models


##Used to see if drone is on platform or not
def check():
    diff = 0
    cap = cv2.VideoCapture(0)
    prev_frame = None
    while diff < 2e7:
        ret, frame = cap.read()
        frame = frame[140:480, 230:610,:]
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if prev_frame is not None:
            diff = (prev_frame - frame).sum()
            print(diff)
        else:   
            prev_frame = frame.copy()
            
    print("drone")
    cap.release()
    cv2.destroyAllWindows()
    
def check_2():
    model = models.Sequential()
    
    model.add(layers.Conv2D(32, (3, 3), activation ='relu', input_shape=(128, 128, 3)))
    model.add(layers.MaxPooling2D((2,2)))
    model.add(layers.Conv2D(16, (3, 3), activation ='relu', input_shape=(63, 63, 32)))
    model.add(layers.MaxPooling2D((2,2)))
    model.add(layers.Conv2D(2, (3, 3), activation ='relu', input_shape=(30, 30, 32)))
    model.add(layers.MaxPooling2D((2,2)))
    model.add(layers.Conv2D(1, (3, 3), activation ='relu'))
    model.add(layers.MaxPooling2D((2,2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(144, activation='relu'))
    model.add(layers.Dense(32, activation='relu'))

    model.add(layers.Dense(2, activation='relu'))
    print(os.listdir())

    model.load_weights("/home/pi/Desktop/model_tf_2")
    
    cap = cv2.VideoCapture(0)
    prev_frame = None
    diff = 0.0
    while diff < 2e7:
        ret, frame = cap.read()
        #frame = frame[140:480, 230:610,:]
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print(checkTF(cv2.resize(frame,(128,128)), model))
            
    print("drone")
    cap.release()
    cv2.destroyAllWindows()
    
def checkTF(img, model):
    pred = model.predict(np.array([img]))[0]
    if pred[0] > pred[1]:
        return "Not in pad"
    return "In Pad"
if __name__ == "__main__":
    check_2()
    
    
    