from __future__ import print_function, absolute_import
import time, math

def turn(lbot, angle=0, verbose=False):
	lbot.setRobotSpeed(lbot.adv, math.radians(angle))
	time.sleep(1)
	if verbose:
		print('~ Learnbot has turned by ' + str(angle) + ' degrees')