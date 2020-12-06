#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")

fswebcam -d /dev/video0 -S 2 -r 2048x1080 --no-banner /home/pi/Hextronics/landingPadCaptures/$DATE.jpg