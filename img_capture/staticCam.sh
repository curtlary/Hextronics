#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam -r 2048x1080 --no-banner ./$DATE.jpg


