import os
import datetime
import sys
import time
import subprocess
from cv.feature_extraction import (
    find_homography,
    apply_homography,
    get_platform_mask,
    decompose_homography,
    find_homography_dbscan,
)
import matplotlib.pyplot as plt

REFERENCE_IMAGE_PATH = "./ref_img.jpg"

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

# get captured image again:
img = plt.imread(abs_file_path)

ref_img = plt.imread(REFERENCE_IMAGE_PATH)
ref_img = ref_img[::-1, :]

plat = get_platform_mask(ref_img)

# match_img, h,  = find_homography(ref_img, img, plat, plat)
matches_img, h, (img_x, img_y) = find_homography_dbscan(ref_img, img)
print(img_x, img_y)
symbol_center = np.array([955, 640])
button_center = np.array([955, 450])
drone_center = np.array([img_x, img_y])
    

offset_center = symbol_center - drone_center
print(offset_center)

dx, dy, angle = decompose_homography(h)
print(dx, dy, angle)