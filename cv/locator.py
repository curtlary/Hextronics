import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.cluster import DBSCAN

from PIL import Image
from pyzbar import pyzbar
import time
from typing import Tuple 
import pickle as pkl
import numpy as np
import cv2
import os
from statistics import mode
    

class DroneLocator:
    
    def __init__(
        self,
        # circle finder params
        rough_radius_range: Tuple[int, int] = (25, 55),
        fine_radius_range: Tuple[int, int] = (30, 67),
        canny_thresholds: Tuple[int, int] = (70, 30),
        qr2but_range: Tuple[int, int] = (163, 193),
        use_color_filter: bool = True,
        button_color_hsv_low: Tuple[int, int, int] = (15, 50, 100),
        button_color_hsv_high: Tuple[int, int, int] = (40, 255, 255),
        # drone info params
        seek_center: Tuple[int, int] = (980, 837), # pixel coordinates of 0,0,0 quad
        angle_offset: int = 87,
        linreg_path: str = "offset_model.pkl",
        #linreg_path: str = "../cv/offset_model.pkl",
        # Image manipulations
        do_clahe: bool = True,
        do_thres: bool = True,
        do_morph: bool = True, # erode, dilate, etc...
        morph_kernel: int = 3,
        # debug
        show_circles: bool = False,
    ):
        self.rough_radius_range = rough_radius_range
        self.fine_radius_range = fine_radius_range
        self.canny_thresholds = canny_thresholds
        self.qr2but_range = qr2but_range
        self.do_show_circles = show_circles
        self.angle_offset = angle_offset
        
        # script_dir = os.path.dirname(__file__)
        # total_linreg_path = os.path.join(script_dir, linreg_path)
        total_linreg_path = linreg_path
        self.offset_model = pkl.load(open(total_linreg_path, "rb"))
        
        self.do_clahe = do_clahe
        self.do_thres = do_thres
        self.do_morph = do_morph
        self.morph_kernel = np.ones((morph_kernel, morph_kernel), np.uint8)
        
        self.seek_center = np.array(seek_center)
        self.seek_but = np.array(seek_center)
        self.seek_but[1] += 100
        # button
        self.use_color_filter = use_color_filter
        self.hsv_range = (
            button_color_hsv_low,
            button_color_hsv_high,
        )

    def __call__(self, img, with_vis = False, with_video=False):
        old_img = img.copy()
        img = self.process_img(img)
        plt.imshow(img)
        # plt.show()
        # plt.pause(2)
        # plt.close()

        decoded_objs = pyzbar.decode(img)
        circles = self.get_circles(old_img)
        if len(decoded_objs) == 0:
            #if with_vis:
                # plt.title("Couldn't find QR code")
                # plt.imshow(old_img)
                # plt.show(block = False)
                # plt.pause(2)
                # plt.close()
            if with_video:
                return False, 0, 0, 0, old_img
            return False, 0, 0, 0
        qr_center = self.get_qr_center(decoded_objs)

        pred_offset = self.offset_model.predict([self.seek_center - qr_center])[0].round()

        
        if self.do_show_circles:
            self.show_circles(old_img, circles, qr_center)
        if circles is None:
            circle_center = None
        else:
            circle_center = self.matching_circle_center(circles, qr_center)

        angle = 404 # value for not found circle center

        img_ret = old_img.copy()
        if circle_center is not None:
            angle = self.theta(circle_center, qr_center) % 360
            if angle > 180:
                angle = angle -360
            if with_vis:
                self.visualize_results(old_img, circle_center, qr_center, angle, pred_offset)
            if with_video:
                img_ret = self.make_frame(old_img, circle_center, qr_center, angle, pred_offset)
        elif with_vis:
            self.visualize_results(old_img, None, qr_center, "did not find button", pred_offset)

        if circle_center is None and with_video:
            img_ret = self.make_frame(old_img, None, qr_center, "did not find button", pred_offset)

        if with_video:
            return True, pred_offset[0], pred_offset[1], angle, img_ret
        return True, pred_offset[0], pred_offset[1], angle
    
    def visualize_results(self, img, circle_center, qr_center, angle, pred_offset):
        if circle_center is not None:
            plt.scatter(circle_center[0], circle_center[1])
            plt.plot([circle_center[0], qr_center[0] ], [circle_center[1], qr_center[1]])
            cv2.circle(img, (int(circle_center[0]), int(circle_center[1])), 47, (255, 0, 255), 3)
        
        plt.title(f"Pred Offset: {pred_offset}, Angle: {angle}")
        plt.imshow(img)
        plt.scatter(qr_center[0], qr_center[1])
        plt.plot([self.seek_center[0], qr_center[0] ], [self.seek_center[1], qr_center[1]])
        plt.show(block = False)
        plt.pause(1)
        plt.close()

    def scatter(self, img, x, y):
        cv2.circle(img, (x, y), 10, (0, 0, 255), 20)

    def make_frame(self, img, circle_center, qr_center, angle, pred_offset):
        img = img.copy()
        if circle_center is not None:
            cv2.line(img, circle_center[:2], qr_center[:2], (255, 0, 0), 10)
            cv2.circle(img, (int(circle_center[0]), int(circle_center[1])), 47, (255, 0, 255), 3)

        cv2.circle(img, qr_center[:2])
        cv2.line(img, self.seek_center[:2], qr_center[:2], (255, 0, 255), 10)
        return img

    def show_circles(self, img, circles, qr_center=None):
        if self.use_color_filter:
            img = self.color_filt(img)
        
        orig_img = img.copy()
        img = orig_img.copy()
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                cv2.circle(img, center, 1, (0, 100, 100), 3)
                radius = i[2]
                cv2.circle(img, center, radius, (255, 0, 255), 3)

        plt.title("All circles found")
        plt.imshow(img)
       # plt.show()

        img = orig_img.copy()
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0]:
                if qr_center is not None:
                    dist = np.linalg.norm(qr_center - i[:2])
                else:
                    dist = sum(self.fine_radius_range) / 2
                if (
                        self.qr2but_range[0] < dist < self.qr2but_range[1]
                        and self.fine_radius_range[0] < i[2] < self.fine_radius_range[1]
                ):
                    center = (i[0], i[1])
                    cv2.circle(img, center, 1, (0, 100, 100), 3)
                    radius = i[2]
                    cv2.circle(img, center, radius, (0, 255, 255), 3)

        # plt.title("Circles within thresholds")
        # plt.imshow(img)
        # plt.show()
        # plt.pause(2)
        # plt.close()
    
    def get_circles(self, im):
        if self.use_color_filter:
            im = self.color_filt(im)
            # plt.imshow(im)
            # plt.show()
            # plt.pause(2)
            # plt.close()
        n_im = im / 255
        
        #if n_im.sum() <1500:
        #    return None
        rows = im.shape[0]
        # p1, p2 = self.canny_thresholds
        # min_r, max_r = self.rough_radius_range
        # circles = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1, rows / 8,
        #                            param1=p1, param2=p2,
        #                            minRadius=min_r, maxRadius=max_r)
        # if circles is not None:
        #     circles = np.around(circles)
        # return circles
        points = np.where(im > 128)
        points = np.vstack([points[1], points[0]]).T
        
        # clustering = DBSCAN(eps=p1, min_samples=100).fit(points)

        # if np.all(clustering.labels_ == -1):
        #     return []
        # most = mode([i for i in clustering.labels_ if i != -1])
        #
        # cluster_points = np.array([points[j] for j in range(len(points)) if clustering.labels_[j] == most])
        # cluster_points_idx = np.array([j for j in range(len(points)) if clustering.labels_[j] == most])
        oi = points.mean(axis=0)
        print(oi)
        cx, cy = oi
        # cx, cy = cluster_points.mean(axis=1)
        return np.array([[cx, cy, sum(self.fine_radius_range) / 2.]])

    def matching_circle_center(self, circles, qr_center):
        possible = []
        for circle in circles:
            dist = np.linalg.norm(qr_center - circle[:2])
            if (
                self.qr2but_range[0] < dist < self.qr2but_range[1]
                and self.fine_radius_range[0] < circle[2] < self.fine_radius_range[1]
            ): 
                possible.append(circle[:2])
        if len(possible) ==0:
            return None
        return possible[0] # TODO: make it so that you can return all and test which one works best

    def theta(self, circle_center, qr_center):
        vec = qr_center - circle_center.astype(float)
        return np.degrees(np.arctan(vec[1]/vec[0])) + self.angle_offset

    def process_img(self, img):
        """ Applies transforms to the image to make it good
            - Histogram Equalization (Still experimenting)
            - Image dewarping (Planning)
            - thresholding to make QR code more contrastive
            - Dilation + Erosion (Still experimenting)
        """
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        if self.do_thres:
            img = cv2.adaptiveThreshold(
                img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,65,2 
            )
        if self.do_morph:
            img = cv2.dilate(img, self.morph_kernel, iterations = 1)
            img = cv2.erode(img, self.morph_kernel, iterations = 1)
        return img


    def get_qr_center(self, objs):
        for obj in objs: 
            points = obj.polygon

        if len(points) > 4: 
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else: 
            hull = points

        n = len(hull)
        hull = np.array([(p.x, p.y) for p in hull])
        center = hull.mean(axis = 0)
        return center
    
    def imread(self, path):
        img = np.array(plt.imread(path))
       
        if img.max() <= 1:
            img = (img * 255)
        return img.astype(np.uint8)

    def color_filt(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        lower = np.array(self.hsv_range[0])
        upper = np.array(self.hsv_range[1])
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, self.morph_kernel, iterations=2)
        # result = cv2.bitwise_and(img, img, mask=mask)
        return mask

