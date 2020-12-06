#!/usr/bin/env python3
import os
import sys
import time
from os import environ
import subprocess
from serWrite import write
import swap
from scan import main
#from checkPad import check

os.system("cd /home/pi/Hextronics")

while True:
    
    time.sleep(3)
    
    #if(not checkPad()):
    #    continue
    
    print("Drone Landed!")
    
    write("pad_recieve")
    
    print("Scanning!")
    main()
    
    print("Done! Now waiting for 5 mins.")
    time.sleep(300)