from __future__ import division, print_function
import time, math

def turn_left(lbot, duration=0.05, rotSpeed=-0.3, verbose=False):
	lbot.setBaseSpeed(0, rotSpeed)
	if verbose:
		print('~ Learnbot turning left ...')
	if duration != 0:
		time.sleep(duration)
		#lbot.setBaseSpeed(0, 0)

