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


def movecam(arr, count = 0):
    
    if (arr[3] == 404):
        command = "./serialWrite.py movecam_" + to_str(-arr[1]) + "_" + to_str(-arr[2]) + "_0"
    else:
        command = "./serialWrite.py movecam_" + to_str(-arr[1]) + "_" + to_str(-arr[2]) + "_" + to_str(arr[3])
    os.system(command)
    if count > 5 and arr[0] == False:
        main()
    if(abs(arr[1]) < 5 and abs(arr[2]) < 5 and abs(arr[3]) <5 and arr[0] == True):
        swap.write()
        #scan()
        #os.system("./serialWrite.py zero")
    else:
        results = scan()
        if results[0] == True:
            print("oito")
            print(results)
            movecam(results)
        else:
            print("to")
            print(arr)
            arr = list(arr)
            arr[1] /= -2
            arr[2] /= -2
            arr[1] = int(arr[1])
            arr[2] = int(arr[2])
            arr = tuple(arr)
            movecam(arr, count + 1)


def scan():
    # locator = DroneLocator(
    #     linreg_path="cv/offset_model.pkl",
    #     canny_thresholds=(200, 200),
    #     show_circles=False,
    #     rough_radius_range=(20, 60),
    #     fine_radius_range=(30, 60),
    #     qr2but_range=(150, 600),
    #     button_color_hsv_low=(27, 120, 200),
    #     button_color_hsv_high=(35, 180, 255),
    #     do_morph=False,
    #     #do_thres=False,
    # )
    locator = DroneLocator(
        linreg_path="cv/offset_model.pkl",
        canny_thresholds=(100, 10),
        show_circles=False,
        rough_radius_range=(30, 50),
        fine_radius_range=(30, 60),
        qr2but_range=(150, 600),
        button_color_hsv_low=(25, 50, 100),
        button_color_hsv_high=(40, 255, 255),
    )

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
    position = [
        "0_420_90",
        #"0_400_90",
        #"0_380_90",
        "0_350_90",
        #"0_300_90",
        #"-75_300_90",
        #"-125_300_90",
        "-125_350_90",
        "-75_350_90",
        "-75_400_90",
        "-125_400_90",
        "75_400_90",
        "125_400_90",
        "125_350_90",
        "75_350_90",
        #"75_400_90",
        #"125_400_90",
    ]
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
        #os.system("./serialWrite.py moveto_0_350_90")
        os.system("./serialWrite.py zero")
        os.system("./serialWrite.py pad_send")
