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

os.chdir("/home/pi/Hextronics")

write("goto_100_-100_100_-100")

write("pad_send")

write("gripper_open")

write("zero")

os.system("./LPCapture.py")
os.system("./LPCapture.py")
time.sleep(20)
os.system("./LPCapture.py")


os.system("./emptyPadCapture.sh")

while True:

    while True:
        time.sleep(5)
        if(landed.checkPad(100,1500)):
            print("Something's on the pad!")
            if(not landed.checkMotion(15,200)):
                print("It Stopped Moving!")
                break
        print("We're just chillin.")
        
    print("Drone Landed!")

    write("pad_recieve")

    print("Scanning!")
    main()

    print("Done! Now waiting for 5 mins.")
    time.sleep(300)