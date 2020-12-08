#!/usr/bin/env python3
import serial
import time
import sys
import os

def write(command):
    os.system('sudo stty -F /dev/ttyACM0 -hupcl')
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1,dsrdtr=False)
    ser.flush()

    mustend = time.time() + 10
    output = str(command) + " \n"
    ser.write(output.encode('utf-8'))
    while time.time() < mustend:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if(line == "Arrived!"):
                break
