#!/usr/bin/env python3.6
import time
import os
from actuation.actuator import ActuatorController
import cv2
from cv.locator import DroneLocator
from cv.video import VideoMaker, VideoMaker4Thread

class PathPlanner:
    def __init__(
            self,
            controller: ActuatorController,
            locator: DroneLocator,
            video_maker: VideoMaker,
    ):
        self.controller = controller
        self.locator = locator
        self.video = video_maker

    def search_main(self):
        self.controller.goto(4000, -500, 1000, 0)

        anchor_positions = [
            (-125, 225, 90),
            (-75, 300, 90),
            (0, 350, 90),
            (75, 300, 90),
            (125, 225, 90),
        ]

        found = False

        for spot in anchor_positions:
            ret, frame = self.video.get_img()
            self.controller.move_to(*spot)

            found_qr, dx, dy, theta, annotated_frame = self.locator(frame, with_video=True)

            self.video.record_frame(ret, annotated_frame)
            if found_qr:
                print(f"found it around here: {spot}")
                self.direct_line(dx, dy, theta)
                found = True
                break

            print(f"Didn't find it at position: {spot}")

        if not found:
            print("Scan Failed!")
            self.controller.move_to(0, 350, 90)
            self.controller.move_to(0, 350, 90)
            self.controller.zero()

    def direct_line(self, dx, dy, angle):
        if angle == 404:
            angle = 0

        self.controller.move_cam(dx, dy, angle)

        if max(abs(dx), abs(dy), abs(angle)) < 10:
            self.controller.set_step_1()
        else:
            ret, img = self.video.get_img()
            _, dx, dy, angle, annotated_frame = self.locator(img, with_video=True)
            self.video.record_frame(ret, annotated_frame)
            self.direct_line(dx, dy, angle)


class PathPlanner4Thread(PathPlanner):

    def __init__(
            self,
            controller: ActuatorController,
            locator: DroneLocator,
            video_maker: VideoMaker4Thread,
    ):
        super().__init__(controller, locator, video_maker)

    def search_main(self):
        self.controller.goto(4000, -500, 1000, 0)

        anchor_positions = [
            (-125, 225, 90),
            (-75, 300, 90),
            (0, 350, 90),
            (75, 300, 90),
            (125, 225, 90),
        ]

        found = False

        for spot in anchor_positions:
            self.controller.move_to(*spot)

            found_qr, dx, dy, theta, annotated_frame = self.video.get_scan()

            if found_qr:
                print(f"found it around here: {spot}")
                self.direct_line(dx, dy, theta)
                found = True
                break

            print(f"Didn't find it at position: {spot}")

        if not found:
            print("Scan Failed!")
            self.controller.move_to(0, 350, 90)
            self.controller.move_to(0, 350, 90)
            self.controller.zero()

    def direct_line(self, dx, dy, angle):
        if angle == 404:
            angle = 0

        self.controller.move_cam(dx, dy, angle)

        if max(abs(dx), abs(dy), abs(angle)) < 10:
            self.controller.set_step_1()
        else:
            _, dx, dy, angle, annotated_frame = self.video.get_scan()
            self.direct_line(dx, dy, angle)




