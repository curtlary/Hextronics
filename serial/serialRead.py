#!/usr/bin/env python3
import serial
from datetime import datetime

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    
    starttime = datetime.now()
    print(starttime)
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
        timedelta = datetime.now() - starttime
        if timedelta.total_seconds() >= 10:
            break