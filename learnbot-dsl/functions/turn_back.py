import time, math
from __future__ import division

def turn_back(lbot, params=None, verbose=False):
	lbot.setRobotSpeed(lbot.adv, math.pi)
	time.sleep(1)
	if verbose:
		print('~ Learnbot has turned back')