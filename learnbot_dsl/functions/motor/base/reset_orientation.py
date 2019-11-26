from __future__ import print_function, absolute_import
import time, math, numpy

def reset_orientation(lbot, keygyro = "Z_AXIS"):
    lbot.resetGyroscope(keygyro)
    curAngle= lbot.getGyroscope(keygyro)
    if curAngle is not None:
        while curAngle>1:
            curAngle = lbot.getGyroscope(keygyro)

