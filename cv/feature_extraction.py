import cv2
import numpy as np
import matplotlib.pyplot as plt

def find_homography(ref_img, img, ref_mask = None, mask = None):

    orb = cv2.ORB_create()
    
    ref_kpts, ref_des = orb.detectAndCompute(ref_img, ref_mask)
    kpts, des = orb.detectAndCompute(img, mask)

    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    matches = bf.match(ref_des, des)
    matches = sorted(matches, key = lambda x: x.distance)
    matches_img = cv2.drawMatches(
        ref_img, ref_kpts, img, kpts, matches[:50], None,
    )

    # Extract location of good 
    points_ref = np.zeros((len(matches), 2), dtype=np.float32)
    points = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points_ref[i, :] = ref_kpts[match.queryIdx].pt
        points[i, :] = kpts[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points_ref, points, cv2.RANSAC)

    return matches_img, h

def apply_homography(img, h):
    height, width, _ = img.shape
    return cv2.warpPerspective(img, h, (width, height))

def get_platform_mask(img, threshold = (130, 255)):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
    thresh = cv2.threshold(sharpen, threshold[0], threshold[1], cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    op = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=6)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30,30))
    close = cv2.morphologyEx(op, cv2.MORPH_CLOSE, kernel, iterations=2)
    close[close==255] = 1
    return close 