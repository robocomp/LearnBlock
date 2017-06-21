import time, math
#To make it compatible with python 3
from __future__ import print_function
from __future__ import division

def turn_left(lbot, params=None, verbose=True):
	lbot.setRobotSpeed(lbot.adv, -math.pi/2)
	if verbose:
		print('~ Learnbot turning left ...')
	time.sleep(1)