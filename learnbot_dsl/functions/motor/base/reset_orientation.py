from __future__ import print_function, absolute_import
import time, math, numpy

def reset_orientation(lbot, keygyro = "Z_AXIS"):
    if "gyroscope" in lbot.devicesAvailables:
        lbot.resetGyroscope(keygyro)
        curAngle= lbot.getGyroscope(keygyro)
        while curAngle!=0:
            curAngle = lbot.getGyroscope(keygyro)

