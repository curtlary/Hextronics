#!/usr/bin/env python3
import os
import sys
from Scan import main
from readGPIO import readGPIO
import time

while True:
    time.sleep(3)
    print(readGPIO())
    if readGPIO():
        print("INITIATED")
        os.system("./serialWrite.py roof_open")
        time.sleep(20)
        main()
        time.sleep(240)
        os.system("./serialWrite.py roof_close")
        os.system("./serialWrite.py roof_close")
        os.system("./serialWrite.py roof_close")
        break