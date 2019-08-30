from __future__ import division
import time, math

def turn_back(lbot):
	lbot.setBaseSpeed(lbot.getAdv(), 180)
	time.sleep(1)
	lbot.setBaseSpeed(0, 0)
