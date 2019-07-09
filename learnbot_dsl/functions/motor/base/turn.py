from __future__ import print_function, absolute_import
import time, math, numpy

def turn(lbot, angle=0):
    if "gyroscope" in lbot.devicesAvailables:
        lbot.resetGyroscope()
        rx, curAngle, rz = lbot.getGyroscope()
        while curAngle!=0:
            rx, curAngle, rz = lbot.getGyroscope()
        diff = math.fabs(angle) 
        s = numpy.sign(angle)
        curVel = 0
        while math.fabs(curAngle-angle)>2:
            if diff>30:
                angleVel = 30
            else:
                angleVel = diff
            finalVel = angleVel*s
            if curVel!=finalVel:
                lbot.setBaseSpeed(0, math.radians(finalVel/2))
                curVel = finalVel
            time.sleep(0.1)
            rx, curAngle, rz = lbot.getGyroscope()
            diff = math.fabs(curAngle-angle)
            s = numpy.sign(angle-curAngle)
            #print("angle", curAngle)

        lbot.setBaseSpeed(0, 0)
    else:
        if angle > 0:
            if angle > 20:
                angleVel = 20
        else:
            if angle < -20:
                angleVel = -20
        movingTime = angle/angleVel
        lbot.setBaseSpeed(0, math.radians(angleVel))
        time.sleep(movingTime)
        lbot.setBaseSpeed(0, 0)        
