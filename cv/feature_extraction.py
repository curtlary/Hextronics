import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.cluster import DBSCAN
from statistics import mode

def find_homography(ref_img, img, ref_mask = None, mask = None, thres=None):
    # orb = cv2.ORB_create()
    orb = cv2.SIFT_create()

    
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

    if thres:
        points_ref = points_ref[:thres]
        points = points[:thres]
    # Find homography
    # h, mask = cv2.findHomography(points_ref, points, cv2.RANSAC)
    h = cv2.estimateAffinePartial2D(points_ref, points, cv2.RANSAC)[0]
    return matches_img, h

def find_homography_dbscan(ref_img, img, ref_mask = None, mask = None, thres=None):
    orb = cv2.SIFT_create()
    
    ref_kpts, ref_des = orb.detectAndCompute(ref_img, ref_mask)
    kpts, des = orb.detectAndCompute(img, mask)

    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    matches = bf.match(ref_des, des)
    matches = sorted(matches, key = lambda x: x.distance)

    points_ref = np.zeros((len(matches), 2), dtype=np.float32)
    points = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points_ref[i, :] = ref_kpts[match.queryIdx].pt
        points[i, :] = kpts[match.trainIdx].pt

    clustering = DBSCAN(eps=20, min_samples=3).fit(points)
        
    most = mode([i for i in clustering.labels_ if i !=-1])

    cluster_points = np.array([points[j] for j in range(len(points)) if clustering.labels_[j] == most])
    # xs = cluster_points[:, 0]
    # ys = cluster_points[:, 1]
    cx, cy= cluster_points.mean(axis=0)

    mask = np.zeros((img.shape[0], img.shape[1]))
    mask[int(cy-50):int(cy+50), int(cx-50):int(cx+50)] = 1
    mask = mask.astype(np.uint8)
    kpts, des = orb.detectAndCompute(img, mask)

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

    if thres:
        points_ref = points_ref[:thres]
        points = points[:thres]

    # Find homography
    # h, mask = cv2.findHomography(points_ref, points, cv2.RANSAC)
    h = cv2.estimateAffinePartial2D(points_ref, points, cv2.RANSAC)[0]
    return matches_img, h, points.mean(axis=0)


def apply_homography(img, h):
    if h.shape == (2, 3):
        h = np.vstack((h, [0,0,1]))
    height, width, _ = img.shape
    return cv2.warpPerspective(img, h, (width, height))

def get_platform_mask(img, threshold = (130, 255)):
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur = cv2.medianBlur(gray, 5)
    # sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    # sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
    # thresh = cv2.threshold(sharpen, threshold[0], threshold[1], cv2.THRESH_BINARY)[1]
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # op = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=6)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30,30))
    # close = cv2.morphologyEx(op, cv2.MORPH_CLOSE, kernel, iterations=2)
    # close[close==255] = 1
    # return close 
    # Converting image to a binary image  
    # (black and white only image). 
    h,w,_ = img.shape
    mask = np.zeros((h,w))

    mask[:,350:1525] = 1 
    return mask.astype(np.uint8)
   
def decompose_homography(h):
    dx = h[0][2]
    dy = h[1][2]
    angle = - math.atan2(h[0,1], h[0,0]) * 180 / math.pi
    return dx, dy, angle