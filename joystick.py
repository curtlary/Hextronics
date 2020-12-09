from cv.locator import DroneLocator
from cv.video import VideoMaker
from planning.planner import PathPlanner
from actuation.actuator import ActuatorController
import cv2
import time
import os

#controller = ActuatorController()

cap = cv2.VideoCapture(2)

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    k = cv2.waitKey(33)
    if k == ord('q'):
        break
    if k == ord('w'):
        os.system("./serialWrite.py movecam_10_0_0")
        print("w")
    if k == ord('a'):
        os.system("./serialWrite.py movecam_0_10_0")
        print("a")
    if k == ord('d'):
        os.system("./serialWrite.py movecam_0_-10_0")

        print("d")
    if k == ord('s'):
        os.system("./serialWrite.py movecam_-10_0_0")

        print("s")
    if k == ord('z'):
        os.system("./serialWrite.py zero")

        print("s")


cap.release()
cv2.destroyAllWindows()





