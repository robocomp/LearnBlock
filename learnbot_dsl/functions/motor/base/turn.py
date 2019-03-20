from __future__ import print_function, absolute_import
import time, math

def turn(lbot, angle=0):
	lbot.setBaseSpeed(lbot.getAdv(), math.radians(angle))
