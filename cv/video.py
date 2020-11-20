import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import time


class VideoMaker:
    def __init__(self, run_name="Test"):
        self.cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        self.out = cv2.VideoWriter(f'{run_name}.mp4', fourcc, 20.0, (640,480))


    def get_img(self):
        if self.cap.isOpened():
            ret, img = self.cap.read()
            print(ret)
        else:
            print("Camera Module not found")
            # directory for camera image placement
            script_dir = "/home/pi/Hextronics/camera/"

            # call the .sh to capture the image
            os.system('./camCapture.sh')

            # capture the picture's path from the list of files in camera dir
            wd = os.getcwd()
            os.chdir("camera")
            filelist = os.popen("ls")
            text = filelist.read()
            filelist.close
            os.chdir(wd)
            captured_path = str(text[-22:-1])
            # join the absolute path and the captured path
            abs_file_path = os.path.join(script_dir, captured_path)

            print(os.path.basename(abs_file_path))
            img = self.imread(abs_file_path)
            ret = True
        return ret, img


    def imread(self, path):
        img = plt.imread(path)
        if img.max() <= 1:
            img = (img * 255)
        return img.astype(np.uint8)

    def record_frame(self, ret, frame):
        if ret:
            frame = cv2.flip(frame, 0)
            self.out.write(frame)
        #cv2.imshow('Gantry View', frame)
        #cv2.waitKey(1)
        plt.imshow(frame)
        plt.show()
        print("oito")
        time.sleep(5)


    def close(self):
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

class VideoMaker4Thread(VideoMaker):
    def __init__(self, run_name="Test", locator=None):
        super().__init__(run_name)
        _, self.curr_img = self.cap.read()
        self.locator = locator
        self.found_qr = False
        self.dx = 0
        self.dy = 0
        self.angle = 0

    def get_scan(self):
        return self.found_qr, self.dx, self.dy, self.angle, self.curr_img

    def loop(self):
        while self.cap.isOpened():
            print("oi")
            ret, self.curr_img = self.cap.read()
            if ret:
                self.found_qr, self.dx, self.dy, self.angle, frame = self.locator(self.curr_img, with_video=True)
                self.curr_img = frame
                frame = cv2.flip(frame, 0)
                self.out.write(frame)
                cv2.imshow("Gauntry View", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
