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

def find_homography_dbscan(ref_img, img, ref_mask = None, mask = None, thres=None, eps=30, min_samples=3):
    # orb = cv2.ORB_create()
    orb = cv2.SIFT_create()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
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

    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
        
    most = mode([i for i in clustering.labels_ if i !=-1])

    cluster_points = np.array([points[j] for j in range(len(points)) if clustering.labels_[j] == most])
    cluster_points_idx = np.array([j for j in range(len(points)) if clustering.labels_[j] == most])
    cx, cy = cluster_points.mean(axis=0)

    ref_cluster_points = points_ref[cluster_points_idx]
    ref_cx, ref_cy = ref_cluster_points.mean(axis=0)

    scale = 0.5 
    offset_cx = (ref_img.shape[1] // 2 - ref_cx) * scale
    offset_cy = (ref_img.shape[0] // 2 - ref_cy) * scale
    cy += offset_cy
    cx += offset_cx

    mask = np.zeros((img.shape[0], img.shape[1]))
    mask_size = 90
    mask[int(cy-mask_size):int(cy+mask_size), int(cx-mask_size):int(cx+mask_size)] = 1
    mask = mask.astype(np.uint8)

    # masked_img = img.copy()
    # masked_img[np.where(mask == 0)] = 0
    # plt.imshow(masked_img)
    # plt.show()

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
    h,w,_ = img.shape
    mask = np.zeros((h,w))

    mask[:,350:1525] = 1 
    return mask.astype(np.uint8)
   
def decompose_homography(h):
    dx = h[0][2]
    dy = h[1][2]
    angle = - math.atan2(h[0,1], h[0,0]) * 180 / math.pi
    return dx, dy, angle

def full_workflow(img_path, ref_path = "../imgs/shapes/trident/trident ref.png"):
    ref_img = (plt.imread(ref_path) * 255).astype(np.uint8)
    ref_img = ref_img[::-1, :]
    img = plt.imread(img_path)
    ym, yb = (-14.172335600907024, 16755.952380952378)
    xm, xb = (-6.616207060816175, 9863.494415921241)

    matches_img, h, (img_x, img_y) = find_homography_dbscan(ref_img, img)
    # plt.imshow(matches_img)
    # plt.show()
    
    _, __, angle = decompose_homography(h)
    center = (img_x, img_y)

    dist = 190
    drone_center = np.array([img_x, img_y])
    offset_center = [0,0]
    
    angle = -angle
    
    button_center = [drone_center[0] + np.cos(np.radians(90+angle)) * dist, drone_center[1] - np.sin(np.radians(90+angle)) * dist]
        
    offset_center[0] = button_center[0] - drone_center[0]
    offset_center[1] = button_center[1] - drone_center[1]
    but_center = np.array([drone_center[0] + offset_center[0], drone_center[1] + offset_center[1]])
    real_life = [but_center[1] * ym +yb, but_center[0] * xm + xb]

    return real_life, angle
