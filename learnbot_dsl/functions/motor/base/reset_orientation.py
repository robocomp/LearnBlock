from __future__ import print_function, absolute_import
import time, math, numpy

def reset_orientation(lbot):
    if "gyroscope" in lbot.devicesAvailables:
        lbot.resetGyroscope()
        rx, curAngle, rz = lbot.getGyroscope()
        while curAngle!=0:
            rx, curAngle, rz = lbot.getGyroscope()

