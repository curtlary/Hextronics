import cv2
import os
import matplotlib.pyplot as plt
import numpy as np


class VideoMaker:
    def __init__(self, run_name="Test"):
        self.cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(f'{run_name}.avi', fourcc, 20.0, (640,480))

    def get_img(self):
        if self.cap.isOpened():
            ret, img = self.cap.read()
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
        cv2.imshow('Gantry View', frame)

    def close(self):
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()
