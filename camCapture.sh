#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")

fswebcam -S 2 -r 2048x1080 --no-banner /home/pi/Hextronics/camera/$DATE.jpg