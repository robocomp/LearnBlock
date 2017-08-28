from __future__ import division, print_function
import time, math

def turn_right(lbot, duration=0, rotSpeed=0.2, verbose=False):
	lbot.setRobotSpeed(0, rotSpeed)
	if verbose:
		print('~ Learnbot turning right ...')
	if duration != 0:
		time.sleep(duration)
		lbot.setRobotSpeed(0, 0)

