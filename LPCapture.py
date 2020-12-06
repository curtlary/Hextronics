#!/usr/bin/env python3
import os
import datetime
import sys
import time
import subprocess

#read the absolute path
script_dir = "/home/pi/Hextronics/landingPadCaptures/"

#call the .sh to capture the image
os.system('./landingPadCapture.sh')

wd = os.getcwd()
os.chdir("camera")
filelist = os.popen("ls")
text = filelist.read()
filelist.close
os.chdir(wd)
captured_path = str(text[-22:-1])
print(captured_path)

#join the absolute path and the captured path
abs_file_path = os.path.join(script_dir, captured_path)

print(script_dir)
print(abs_file_path)
