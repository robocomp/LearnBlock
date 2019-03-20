from __future__ import division, print_function
import time, math

def turn_90_left(lbot):
	lbot.setBaseSpeed(lbot.getAdv(), -math.pi/2)
	time.sleep(1)
	lbot.setBaseSpeed(lbot.getAdv(), 0)