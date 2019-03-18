from __future__ import division, print_function
import time, math

def turn_90_right(lbot, verbose=False):
	lbot.setBaseSpeed(lbot.getAdv(), math.pi/2)
	if verbose:
		print('~ Learnbot turning right ...')
	time.sleep(1)
	lbot.setBaseSpeed(lbot.getAdv(), 0)
