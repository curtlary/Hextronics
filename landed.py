#!/usr/bin/env python3
import cv2
import time
import os
import imutils
import numpy as np
import matplotlib.pyplot as plt


def imgDiff(img1, img2, threshValue, minArea):
    #img1 = img1[0:300, 0:300]
    img1 = imutils.resize(img1, width = 500)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img1 = cv2.GaussianBlur(img1, (21,21), 0)
    plt.imshow(img1)
    
    plt.show(block = False)
    plt.pause(1)
    plt.close()
    
    #img2 = img1[0:300, 0:300]
    img2 = imutils.resize(img2, width = 500)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.GaussianBlur(img2, (21,21), 0)
    plt.imshow(img2)
    
    plt.show(block = False)
    plt.pause(1)
    plt.close()
    
    #cv2.accumulateWeighted(img1, img2, 0.5)
    frameDelta = cv2.absdiff(img1, img2)
    
    thresh = cv2.threshold(frameDelta, threshValue, 255, cv2.THRESH_BINARY)[1]
    
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2. RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    different = False
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < minArea:
            continue
        different = True
        return(different)
    
    
    
def checkPad(threshValue, minArea):
    #directory for camera image placement
    script_dir = "/home/pi/Hextronics/landingPadCaptures/"

    #call the .sh to capture the image
    os.system('./landingPadCapture.sh')

    #capture the picture's path from the list of files in camera dir
    wd = os.getcwd()
    os.chdir("landingPadCaptures")
    filelist = os.popen("ls")
    text = filelist.read()
    filelist.close
    os.chdir(wd)
    captured_path = str(text[-22:-1])

    #join the absolute path and the captured path
    abs_file_path = os.path.join(script_dir, captured_path)

    print(os.path.basename(abs_file_path))
    
    newImg = cv2.imread(abs_file_path)
    
    newImg = newImg[300:700, 800:1500]
#     cv2.imshow("Cropped", newImg)
#     cv2.waitKey(0)
    
    OGImg = cv2.imread("/home/pi/Hextronics/emptyLandingPad.jpg")
    OGImg = OGImg[300:700, 800:1500]
    
    return imgDiff(newImg, OGImg, threshValue, minArea)
    
    
    
    
def checkMotion(threshValue, minArea):
    #directory for camera image placement
    script_dir = "/home/pi/Hextronics/landingPadCaptures/"

    #dont call the .sh to capture the image
    #os.system('./landingPadCapture.sh')

    #capture the recent picture's path from the list of files in camera dir
    wd = os.getcwd()
    os.chdir("landingPadCaptures")
    filelist = os.popen("ls")
    text = filelist.read()
    filelist.close
    os.chdir(wd)
    captured_path = str(text[-22:-1])

    #join the absolute path and the captured path
    abs_file_path = os.path.join(script_dir, captured_path)
    
    Image1 = cv2.imread(abs_file_path)
    Image1 = Image1[300:400, 800:1500]
    
    time.sleep(1)
    
    #directory for camera image placement
    script_dir = "/home/pi/Hextronics/landingPadCaptures/"

    #call the .sh to capture the image
    os.system('./landingPadCapture.sh')

    #capture the picture's path from the list of files in camera dir
    wd = os.getcwd()
    os.chdir("landingPadCaptures")
    filelist = os.popen("ls")
    text = filelist.read()
    filelist.close
    os.chdir(wd)
    captured_path = str(text[-22:-1])

    #join the absolute path and the captured path
    abs_file_path = os.path.join(script_dir, captured_path)
    
    Image2 = cv2.imread(abs_file_path)
    Image2 = Image2[300:400, 800:1500]
    
    return imgDiff(Image1, Image2, threshValue, minArea)
    