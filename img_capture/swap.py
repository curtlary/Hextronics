#!/usr/bin/env python3
import os
import sys
from datetime import datetime

def wait(time):
    starttime = datetime.now()        
    while True:
        timedelta = datetime.now() - starttime
        if timedelta.total_seconds() >= time:
            break
    return

def storeBattery1():
    os.system('./serial/serialWrite.py goto_225_1300_0')
    print("Going to Battery1!")
    wait(10)
    os.system('./serial/serialWrite.py gripper_open')
    print("Releasing to Battery1!")
    wait(4)
    os.system('./serial/serialWrite.py goto_1500_1300_0')
    os.system('./serial/serialWrite.py battery_raise')
    print("Securing  Battery1!")
    wait(5)
    os.system('./serial/serialWrite.py battery_raise')
    wait(5)
    os.system('./serial/serialWrite.py battery_lower')
    wait(5)
    os.system('./serial/serialWrite.py battery_lower')
    wait(5)
    return

def getBattery4():
    os.system('./serial/serialWrite.py goto_2500_1300_0')
    print("Going to Battery3!")
    wait(3)
    os.system('./serial/serialWrite.py goto_2500_5200_0')
    print("Getting Battery3!")
    wait(2)
    os.system('./serial/serialWrite.py goto_350_5200_0')
    wait(1)
    os.system('./serial/serialWrite.py battery_raise')
    wait(5)
    os.system('./serial/serialWrite.py battery_raise')
    wait(5)
    os.system('./serial/serialWrite.py gripper_close')
    wait(5)
    os.system('./serial/serialWrite.py gripper_close')
    wait(5)
    os.system('./serial/serialWrite.py battery_lower')
    wait(5)
    os.system('./serial/serialWrite.py battery_lower')
    wait(5)
    return

os.system('sudo stty -F /dev/ttyACM0 -hupcl')

os.system('./serial/serialWrite.py goto_0')
wait(10)

os.system('./serial/serialWrite.py goto_2000_0_0')
wait(1)

x = str(sys.argv[1])
y = str(sys.argv[2])
theta = str(sys.argv[3])


gotoLocation = './serial/serialWrite.py goto_' + x +'_' + y + '_' + theta;

print(gotoLocation)
os.system(gotoLocation)
print("x y theta moving!")
wait(9)

os.system('./serial/serialWrite.py zgo_7700')
print("z moving!")
wait(40)

os.system('./serial/serialWrite.py gripper_close')
print("gripping!")
wait(5)

os.system('./serial/serialWrite.py gripper_close')
print("gripping!")
wait(5)


os.system('./serial/serialWrite.py zgo_0')
print("z moving!")
wait(10)

storeBattery1()

getBattery4()

os.system(gotoLocation)

wait(7)
os.system('./serial/serialWrite.py zgo_3000')
wait(20)
os.system('./serial/serialWrite.py jiggle_start')
os.system('./serial/serialWrite.py zgo_6000')
wait(10)
os.system('./serial/serialWrite.py jiggle_stop')

os.system('./serial/serialWrite.py gripper_open')
wait(4)
os.system('./serial/serialWrite.py zgo_4000')
wait(10)
os.system('./serial/serialWrite.py goto_10250_3200_0')
wait(2)
os.system('./serial/serialWrite.py zgo_8500')
wait(25)

os.system('./serial/serialWrite.py zgo_0')
wait(15)
os.system('./serial/serialWrite.py goto_2000_0_0')
wait(7)
os.system('./serial/serialWrite.py goto_0')




    

