#!/usr/bin/env python3
#%reload_ext autoreload
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
import swap


def movecam(arr):
    if (arr[3] == 404):
        command = "./serialWrite.py movecam_-" + to_str(arr[1]) + "_-" + to_str(arr[2]) + "_0"
    else:
        command = "./serialWrite.py movecam_-" + to_str(arr[1]) + "_-" + to_str(arr[2]) + "_-" + to_str(arr[3])
    os.system(command)
    if(abs(arr[1]) < 10 and abs(arr[2]) < 10 and abs(arr[3]) <10):
        swap()
        #scan()
        #os.system("./serialWrite.py zero")
    else:
        movecam(scan())


def scan():
    locator = DroneLocator()

    #directory for camera image placement
    script_dir = "/home/pi/Hextronics/endEffectorCaptures/"

    #call the .sh to capture the image
    os.system('./endEffectorCapture.sh')

    #capture the picture's path from the list of files in camera dir
    wd = os.getcwd()
    os.chdir("endEffectorCaptures")
    filelist = os.popen("ls")
    text = filelist.read()
    filelist.close
    os.chdir(wd)
    captured_path = str(text[-22:-1])

    #join the absolute path and the captured path
    abs_file_path = os.path.join(script_dir, captured_path)

    print(os.path.basename(abs_file_path))

    img = locator.imread(abs_file_path)
    #plt.figure(figsize=(10,10))
    results = locator(img,True)
    return results


def to_str(var):
    return str(list(np.reshape(np.asarray(var), (1, np.size(var)))[0]))[1:-1]

def main():
    position = ["0_420_90", "75_400_90", "-75_400_90", "-125_400_90", "125_400_90"]
    found = False
    for spot in position:
        command = "./serialWrite.py moveto_" + spot
        print(command)
        os.system(command)
        results = scan()
        print(results)
        if(results[0]):
            print("Found it around here: " + spot)
            found = True
            movecam(results)
            break

        print("Didn't find it at position: " + spot)
    if(not found):
        print("Scan Failed!")
        os.system("./serialWrite.py moveto_0_350_90")
        os.system("./serialWrite.py zero")
