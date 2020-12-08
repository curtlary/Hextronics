#!/usr/bin/env python3
import serial
import time
import sys
import os
from datetime import datetime

os.system('sudo stty -F /dev/ttyACM0 -hupcl')

def write():
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1,dsrdtr=False)
    ser.flush()

    output = "swap" + " \n"
    ser.write(output.encode('utf-8'))
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if(line == "Ready to Fly!"):
                break
        