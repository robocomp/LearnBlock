import time, math
from __future__ import division, print_function

def set_turn_right(lbot, params=None, verbose=False):
	lbot.setRobotSpeed(lbot.adv, math.pi/2)
	if verbose:
		print('~ Learnbot turning right ...')
	time.sleep(1)