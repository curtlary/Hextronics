"""
implements perspective transform functionality

Perspective transforms will be used to change the image plane to 
    a top-down view of the hexagon platform
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
from .utils import order_coords, make_hexagon_coords

def get_tpdn_hexagon(
    img_path: str,
    side_length: int = 500,
    calibrated_coords: np.ndarray = None,
) -> np.ndarray:
    if calibrated_coords is None:
        calibrated_coords = calibrate_hexagon_coords(img_path)

    calibrated_coords = order_coords(calibrated_coords)
    tpdn_coords = order_coords(
        make_hexagon_coords(side_length=side_length)
    )
    o = np.array([calibrated_coords[i] for i in [0, 1, 2, 3]])
    tpdn = np.array([tpdn_coords[i] for i in [0, 1, 2, 3]])
    img = plt.imread(img_path)    

    M = cv2.getPerspectiveTransform(
        o[:, ::-1].astype(np.float32),
        tpdn[:, ::-1].astype(np.float32),
    )

    img_size = (
        tpdn[:, 1].max() - tpdn[:, 1].min(),
        tpdn[:, 0].max() - tpdn[:, 0].min(),
    )
    warped = cv2.warpPerspective(img, M, img_size)

    return warped

def calibrate_hexagon_coords(img_path: str) -> np.ndarray:
    return np.array([0, 0])
