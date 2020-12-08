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

while True:

    while True:
        if(landed.checkPad(20,300)):
            print("Something's on the pad!")
            if(not landed.checkMotion(20,300)):
                print("It Stopped Moving!")
        print("We're just chillin.")
        time.sleep(5)