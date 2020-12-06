#!/usr/bin/env python3
import os
import sys
from Scan2 import main
from readGPIO import readGPIO
from serialWrite import write
import time
import cv2

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('run.avi', fourcc, 20.0, (640, 480))

while True:
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame, 0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break

    time.sleep(3)
    print(readGPIO())
    if readGPIO():
        print("INITIATED")
        write("roof_open")
        time.sleep(20)
        main(cap)
        time.sleep(240)
        write("roof_close")
        write("roof_close")
        write("roof_close")
        break
cap.release()
out.release()
cv2.destroyAllWindows()
