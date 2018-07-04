from __future__ import division, print_function
import time, math

def turn_90_right(lbot, verbose=False):
	lbot.rot= math.pi/2
	lbot.setRobotSpeed(lbot.adv, lbot.rot)
	lbot.publish_topic("turn_90_right")
	if verbose:
		print('~ Learnbot turning right ...')
	time.sleep(1)
	lbot.rot= 0
