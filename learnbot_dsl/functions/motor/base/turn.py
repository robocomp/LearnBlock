from __future__ import print_function, absolute_import
import time, math, numpy

def turn(lbot, angle=0):
    if lbot.getGyroscope("Z_AXIS") is not None:
        lbot.resetGyroscope("Z_AXIS")
        curAngle = lbot.getGyroscope("Z_AXIS")
        while curAngle>2:
            curAngle = lbot.getGyroscope("Z_AXIS")

        curAngle = lbot.getGyroscope("Z_AXIS")
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
                curAngle = lbot.getGyroscope("Z_AXIS")
                diff = math.fabs(curAngle-angle)
                s = numpy.sign(angle-curAngle)
                print("angle", curAngle)

            lbot.setBaseSpeed(0, 0)
            time.sleep(1)
            curAngle = lbot.getGyroscope("Z_AXIS")
            diff = math.fabs(curAngle-angle)
            if diff>1:
                s = numpy.sign(angle-curAngle)
                curVel = 0
            else:
                keep_turning = False
            print("angle after stopping", curAngle)
    else:
        angleVel = angle
        if angle > 0:
            if angle > 20:
                angleVel = 20
        else:
            if angle < -20:
                angleVel = -20
        if angleVel!=0:
            movingTime = angle/angleVel
            lbot.setBaseSpeed(0, angleVel)
            time.sleep(movingTime)
            lbot.setBaseSpeed(0, 0)        
