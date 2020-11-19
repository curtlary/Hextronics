#!/usr/bin/env python3
import serial
import time
import sys
import os
from datetime import datetime

os.system('sudo stty -F /dev/ttyACM0 -hupcl')

def write(command):
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1,dsrdtr=False)
    ser.flush()

    starttime = datetime.now()
    output = str(command) + " \n"
    ser.write(output.encode('utf-8'))
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if(line == "Arrived!"):
                break
        timedelta = datetime.now() - starttime
        if timedelta.total_seconds() >= 10:
            break


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1,dsrdtr=False)
    ser.flush()

    starttime = datetime.now()
    #print(starttime)

    output = str(sys.argv[1]) + " \n"
    #print(output)
    ser.write(output.encode('utf-8'))

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if(line == "Arrived!"):
                break
        timedelta = datetime.now() - starttime
        if timedelta.total_seconds() >= 10:
            break