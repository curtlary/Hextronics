#!/usr/bin/env python3
import os
from cv.locator import DroneLocator
import numpy as np
from serialWrite import write


def movecam(arr, cap):
    x, y, angle = arr[1:3]

    if (angle == 404):
        angle = 0
    command = f"movecam_{x}_{y}_{angle}"
    # os.system(command)
    write(command)
    if (abs(x) < 10 and abs(y) < 10 and abs(angle) < 10):
        write("setStep_1")
        return True
    else:
        results = scan(cap)
        if not results[0]:
            return False
        return movecam(results, cap)

def scan(cap):
    locator = DroneLocator()

    if cap.isOpened():
        ret, img = cap.read()
    else:
        print("Camera Module not found")
        # directory for camera image placement
        script_dir = "/home/pi/Hextronics/camera/"

        # call the .sh to capture the image
        os.system('./camCapture.sh')

        # capture the picture's path from the list of files in camera dir
        wd = os.getcwd()
        os.chdir("camera")
        filelist = os.popen("ls")
        text = filelist.read()
        filelist.close
        os.chdir(wd)
        captured_path = str(text[-22:-1])

        # join the absolute path and the captured path
        abs_file_path = os.path.join(script_dir, captured_path)

        print(os.path.basename(abs_file_path))

        img = locator.imread(abs_file_path)
        # plt.figure(figsize=(10,10))
    results = locator(img, True)
    return results


def to_str(var):
    return str(list(np.reshape(np.asarray(var), (1, np.size(var)))[0]))[1:-1]

def main(cap):
    write("goto_4000_-500_1000_0")
    position = ["-125_225_90", "-75_300_90", "0_350_90", "75_300_90", "125_225_90"]
    found = False
    i = 0
    while not found:
        spot = position[i]
        command = "moveto_" + spot
        write(command)
        results = scan(cap)
        print(results)
        if (results[0]):
            print("found it around here: " + spot)
            found = True
            movecam(results, cap)
        i += 1
        i %= len(position)
        print("Didn't find it at position: " + spot)
    print("Scan Failed!")
    write("moveto_0_350_90")
    write("zero")

