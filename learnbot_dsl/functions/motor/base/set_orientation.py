from __future__ import print_function, absolute_import
import time, math, numpy

def set_orientation(lbot, angle=0):
    curAngle = lbot.getGyroscope("Z_AXIS")
    if curAngle is not None:
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
                finalVel = (angleVel*s)/2
                if curVel!=finalVel:
                    lbot.setBaseSpeed(0, finalVel)
                    curVel = finalVel
                time.sleep(0.1)
                curAngle = lbot.getGyroscope("Z_AXIS")
                diff = math.fabs(curAngle-angle)
                s = numpy.sign(angle-curAngle)

            lbot.setBaseSpeed(0, 0)
            time.sleep(1)
            curAngle = lbot.getGyroscope("Z_AXIS")
            diff = math.fabs(curAngle-angle)
            if diff>2:
                s = numpy.sign(angle-curAngle)
                curVel = 0
            else:
                keep_turning = False

