from __future__ import print_function

def stop_bot(lbot, params=None, verbose=False):
	lbot.adv, lbot.rot = 0,0
	lbot.setRobotSpeed(lbot.adv, lbot.rot)
	if verbose:
		print('~ Learnbot stopped')
