from cv.locator import DroneLocator
from cv.video import VideoMaker
from planning.planner import PathPlanner
from actuation.actuator import ActuatorController
import cv2
import time

# controller = ActuatorController()

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('w'):
        print("w")
    if cv2.waitKey(1) & 0xFF == ord('a'):
        print("a")
    if cv2.waitKey(1) & 0xFF == ord('d'):
        print("d")
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print("s")


cap.release()
cv2.destroyAllWindows()





