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
    
    
def movecam(arr):
    if (arr[3] == 404):
        command = "./serialWrite.py movecam_" + to_str(arr[1]) + "_" + to_str(arr[2]) + "_0"
    else:
        command = "./serialWrite.py movecam_" + to_str(arr[1]) + "_" + to_str(arr[2]) + "_" + to_str(arr[3])
    os.system(command)
    if(abs(arr[1]) < 10 and abs(arr[2]) < 10 and abs(arr[3]) <10): 
        os.system("./serialWrite.py setStep_1")
        #scan()
        #os.system("./serialWrite.py zero")
    else:
        movecam(scan())  
        
    
def scan():
    locator = DroneLocator()
    
    #directory for camera image placement
    script_dir = "/home/pi/Hextronics/camera/"

    #call the .sh to capture the image
    os.system('./camCapture.sh')

    #capture the picture's path from the list of files in camera dir
    wd = os.getcwd()
    os.chdir("camera")
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
    os.system("./serialWrite.py goto_4000_-500_1000_0")
    position = ["-125_225_90", "-75_300_90", "0_350_90", "75_300_90", "125_225_90"]
    found = False
    for spot in position:
        command = "./serialWrite.py moveto_" + spot
        os.system(command)
        results = scan()
        print(results)
        if(results[0]):
            print("found it around here: " + spot)
            found = True
            movecam(results)
            break
        
        print("Didn't find it at position: " + spot)
    if(not found):
        print("Scan Failed!")
        os.system("./serialWrite.py moveto_0_350_90")
        os.system("./serialWrite.py zero")

