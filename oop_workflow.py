from cv.locator import DroneLocator
from cv.video import VideoMaker
from planning.planner import PathPlanner
from actuation.actuator import ActuatorController
import cv2
import time
from readGPIO import readGPIO

controller = ActuatorController()
locator = DroneLocator()
video_maker = VideoMaker(run_name="test")
planner = PathPlanner(locator=locator, controller=controller, video_maker=video_maker)

while True:
    time.sleep(3)
    print(readGPIO())

    if readGPIO():
        print("INITIATED")
        controller.open_roof()
        time.sleep(20)
        planner.search_main()
        time.sleep(240)
        controller.close_roof()
        controller.close_roof()
        controller.close_roof()
        break
video_maker.close()




