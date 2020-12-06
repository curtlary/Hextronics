import threading
from cv.locator import DroneLocator
from cv.video import VideoMaker4Thread
from planning.planner import PathPlanner4Thread
from actuation.actuator import ActuatorController
import cv2
import time

controller = ActuatorController()
locator = DroneLocator()
video_maker = VideoMaker4Thread(run_name="test", locator = locator)
planner = PathPlanner4Thread(
    locator=locator, controller=controller, video_maker=video_maker
)

def main():
    while True:
        time.sleep(3)
        #print(readGPIO())

        if True:#readGPIO():
            print("INITIATED")
            controller.open_roof()
            time.sleep(20)
            planner.search_main()
            time.sleep(240)
            controller.close_roof()
            controller.close_roof()
            controller.close_roof()
        if 0xFF == ord('q'):
            break


try:
    oi = threading.Thread(target=main, args=())
    to = threading.Thread(target=video_maker.loop, args=())

    oi.start()
    to.start()

except:
    print("Error")







