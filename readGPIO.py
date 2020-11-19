#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

def readGPIO():
    inputPin = 26
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(inputPin, GPIO.IN)
    state = GPIO.input(inputPin)
    print ('Input = ', state)
    return state
    GPIO.cleanup()
