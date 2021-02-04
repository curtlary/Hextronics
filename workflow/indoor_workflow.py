#!/usr/bin/env python3
import os
import sys
import time
from os import environ
import subprocess
from serWrite import write
import swap
from scan import main
import landed

write("goto_100_-100_100_-100")
write("pad_send")
write("gripper_open")
write("zero")
cap = cv2.VideoCapture(2)
time.sleep(20)
while True:
    while True:
        time.sleep(5)
        if (landed.checkPad(100, 1500)):
            print("Something's on the pad!")
            if (not landed.checkMotion(15, 200)):
                print("It Stopped Moving!")
                break
        print("We're just chillin.")
    write("pad_recieve")
    main()
    time.sleep(300)
