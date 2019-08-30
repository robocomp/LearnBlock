from __future__ import print_function, absolute_import
import time, math, numpy

def turn(lbot, angle=0):
    if "gyroscope" in lbot.devicesAvailables:
        lbot.resetGyroscope()
        rx, curAngle, rz = lbot.getGyroscope()
        while curAngle!=0:
            rx, curAngle, rz = lbot.getGyroscope()

        rx, curAngle, rz = lbot.getGyroscope()
        diff = math.fabs(angle) 
        s = numpy.sign(angle)
        curVel = 0
        keep_turning = True
        while keep_turning:
            while math.fabs(curAngle-angle)>1:
                if diff>30:
                    angleVel = 30
                else:
                    angleVel = diff
                if angleVel < 10:
                    angleVel = 10            
                finalVel = (angleVel*s)
                if curVel!=finalVel:
                    lbot.setBaseSpeed(0, finalVel)
                    curVel = finalVel
                time.sleep(0.1)
                rx, curAngle, rz = lbot.getGyroscope()
                diff = math.fabs(curAngle-angle)
                s = numpy.sign(angle-curAngle)
                print("angle", curAngle)

            lbot.setBaseSpeed(0, 0)
            time.sleep(1)
            rx, curAngle, rz = lbot.getGyroscope()
            diff = math.fabs(curAngle-angle)
            if diff>1:
                s = numpy.sign(angle-curAngle)
                curVel = 0
            else:
                keep_turning = False
            print("angle after stopping", curAngle)
    else:
        if angle > 0:
            if angle > 20:
                angleVel = 20
        else:
            if angle < -20:
                angleVel = -20
        movingTime = angle/angleVel
        lbot.setBaseSpeed(0, angleVel)
        time.sleep(movingTime)
        lbot.setBaseSpeed(0, 0)        
