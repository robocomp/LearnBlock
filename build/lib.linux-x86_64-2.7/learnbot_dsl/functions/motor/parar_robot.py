from __future__ import print_function

def parar_robot(lbot, params=None, verbose=False):
	lbot.adv, lbot.rot = 0,0
	lbot.setRobotSpeed(lbot.adv, lbot.rot)
	lbot.publish_topic("parar_robot")
	if verbose:
		print('~ Learnbot stopped')
