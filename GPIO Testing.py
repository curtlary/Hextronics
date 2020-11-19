#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

inputPin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(inputPin, GPIO.IN)

while True:
    state = GPIO.input(inputPin)
    print ('Input = ', state)
    time.sleep(2)
    
GPIO.cleanup()
