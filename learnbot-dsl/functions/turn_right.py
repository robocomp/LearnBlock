import time, math
#To make it compatible with python 3
from __future__ import print_function
from __future__ import division

def set_turn_right(lbot, params=None, verbose=False):
	lbot.setRobotSpeed(lbot.adv, math.pi/2)
	if verbose:
		print('~ Learnbot turning right ...')
	time.sleep(1)