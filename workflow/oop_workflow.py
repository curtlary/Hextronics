from ..cv.locator import DroneLocator
from ..cv.video import VideoMaker
from ..planning.planner import PathPlanner
from ..actuation.actuator import ActuatorController
import cv2
import time
from readGPIO import readGPIO

controller = ActuatorController()
locator = DroneLocator(
    linreg_path="cv/offset_model.pkl",
    canny_thresholds=(200, 200),
    show_circles=False,
    rough_radius_range=(20, 60),
    fine_radius_range=(30, 60),
    qr2but_range=(150, 600),
    button_color_hsv_low=(25, 50, 100),
    button_color_hsv_high=(40, 255, 255),
)
video_maker = VideoMaker(run_name="test")
planner = PathPlanner(locator=locator, controller=controller, video_maker=video_maker)

while True:
    time.sleep(3)
    print(readGPIO())

    if readGPIO():
        print("INITIATED")
        controller.open_roof()
        time.sleep(20)
        planner.wait()
        planner.search_main()
        time.sleep(240)
        controller.close_roof()
        controller.close_roof()
        controller.close_roof()
        break
video_maker.close()




