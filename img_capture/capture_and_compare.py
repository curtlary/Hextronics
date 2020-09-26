import os
import datetime
import sys
import time
import subprocess
from cv.feature_extraction import find_homography, apply_homography, get_platform_mask
import matplotlib.pyplot as plt

#read the absolute path
script_dir = os.path.dirname(__file__)

#call the .sh to capture the image
os.system('./staticCam.sh')

#get the date and time, set the date and teim as a filename
currentdate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")

#create the realpath
rel_path = currentdate +".jpg"

#join the absolute path and created file name
abs_file_path = os.path.join(script_dir, rel_path)

#get captured image again:
img = plt.imread(abs_file_path)
plat = get_platform_mask(img)

plt.imshow(img)
plt.show()
plt.imshow(plat)
plt.show()

