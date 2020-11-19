import cv2
import numpy as np

def dewarp(im):
    w, h = im.shape[:2]
    distCoeff = np.zeros((4,1),np.float64)

    # TODO: add your coefficients here!
    k1 = -1.0e-5 # negative to remove barrel distortion
    k2 = 0
    p1 = -1.0e-4
    p2 = -1.0e-4

    distCoeff[0,0] = k1
    distCoeff[1,0] = k2
    distCoeff[2,0] = p1
    distCoeff[3,0] = p2

    # assume unit matrix for camera
    cam = np.eye(3,dtype=np.float32)

    cam[0,2] = w / 2.0  # define center x
    cam[1,2] = h / 2.0  # define center y
    cam[0,0] = 10.      # define focal length x
    cam[1,1] = 6.      # define focal length y

    # here the undistortion will be computed
    img = cv2.undistort(im,cam,distCoeff)
    return img
