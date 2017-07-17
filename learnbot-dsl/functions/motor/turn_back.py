from __future__ import division
import time, math

def turn_back(lbot, verbose=False):
	lbot.rot= math.pi
	lbot.setRobotSpeed(lbot.adv, lbot.rot)
	if verbose:
		print('~ Learnbot turning back ...')
	time.sleep(1)
	lbot.rot=0
	if verbose:
		print('~ Learnbot has turned back')
	