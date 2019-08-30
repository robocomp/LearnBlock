from __future__ import division, print_function
import time, math

def turn_90_right(lbot):
	lbot.setBaseSpeed(lbot.getAdv(), 90)
	time.sleep(1)
	lbot.setBaseSpeed(lbot.getAdv(), 0)
