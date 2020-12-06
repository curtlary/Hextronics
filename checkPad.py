#!/usr/bin/env python3
import os
from os import environ
import sys
import time
import subprocess
import datetime
from cv.locator import DroneLocator
import matplotlib.pyplot as plt
import numpy as np
import cv2


##Used to see if drone is on platform or not
def check():
    