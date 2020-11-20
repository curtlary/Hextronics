#!/usr/bin/env python3
import serial
from datetime import datetime
from typing import Union
import os

os.system('sudo stty -F /dev/ttyACM0 -hupcl')

class ActuatorController:
    def __init__(
            self,
            serial_port: str = "/dev/ttyACM0",
            serial_timeout: int = 1,
            serial_rate: int = 115200,
    ):
        self.ser = serial.Serial(
            serial_port, serial_rate, timeout=serial_timeout, dsrdtr=False
        )

    def write(self, command):
        return True
#        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1,dsrdtr=False)
#        self.ser.flush()
#
#        starttime = datetime.now()
#        output = str(command) + " \n"
#        self.ser.write(output.encode('utf-8'))
#        while True:
#            if self.ser.in_waiting > 0:
#                line = self.ser.readline().decode('utf-8').rstrip()
#                print(line)
#                if(line == "Arrived!"):
#                    break
#            timedelta = datetime.now() - starttime
#            if timedelta.total_seconds() >= 10:
#                break

    def move_to(self, x: Union[int, str], y: Union[int, str], theta: Union[int, str]):
        if not(type(x) is str or type(x) is int):
            x, y, theta = int(x), int(y), int(theta)
        self.write(f"moveto_{x}_{y}_{theta}")

    def move_cam(self, x: Union[int, str], y: Union[int, str], theta: Union[int, str]):
        if not(type(x) is str or type(x) is int):
            x, y, theta = int(x), int(y), int(theta)
        self.write(f"movecam_{x}_{y}_{theta}")

    def goto(self, x: Union[int, str], y: Union[int, str], z: Union[int, str], theta: Union[int, str]):
        if not(type(x) is str or type(x) is int):
            x, y, z, theta = int(x), int(y), int(z), int(theta)
        self.write(f"goto_{x}_{y}_{z}_{theta}")

    def zero(self):
        self.write("zero")

    def set_step_1(self):
        self.write("setStep_1")

    def open_roof(self):
        self.write("roof_open")

    def close_roof(self):
        self.write("roof_close")

