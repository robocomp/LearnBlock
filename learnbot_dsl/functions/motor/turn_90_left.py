from __future__ import division, print_function
import time, math

def turn_90_left(lbot, verbose=False):
	lbot.setBaseSpeed(lbot.getAdv(), -math.pi/2)
	if verbose:
		print('~ Learnbot turning left ...')
	time.sleep(1)
	lbot.setBaseSpeed(lbot.getAdv(), 0)