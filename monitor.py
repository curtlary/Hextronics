#!/usr/bin/env python3
import numpy as np
from cv.locator import DroneLocator
import cv2


cap = cv2.VideoCapture(2)
locator = DroneLocator(
    linreg_path="cv/offset_model.pkl",
    canny_thresholds=(100, 10),
    show_circles=False,
    rough_radius_range=(30, 50),
    fine_radius_range=(30, 60),
    qr2but_range=(150, 600),
    button_color_hsv_low=(25, 50, 100),
    button_color_hsv_high=(40, 255, 255),
)
while(True):
    ret, frame = cap.read()
    qr, x, y, angle = locator(frame)
    if qr:
        if angle == 404:
            cv2.circle(frame, [x, y], (255, 0, 0), 10)
            cv2.circle(frame, [x, y], (255, 0, 0), 10)
            cv2.putText(
                frame,
                str(angle),
                (x + 10, y + 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (128, 255, 255),
                2,
            )
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

