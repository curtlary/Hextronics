#!/usr/bin/env python3
import os
import sys
from time import sleep
import Rpi.GPIO as GPIO

GPIO.setmode(GPIO.BC)
INPUT_PIN = 26
GPIO.setup(INPUT_PIN, GPIO.IN)

open = False

while True:
    if(GPIO.input(INPUT_PIN) == True):
        if(not(open)):
            os.system('./serial/serialWrite.py roof_open')            
            os.system('./serial/serialWrite.py battery_raise')
    if(GPIO.input(INPUT_PIN) == False):
        if(open):
            os.system('./serial/serialWrite.py roof_close')
            os.system('./serial/serialWrite.py battery_lower')
    sleep(1)