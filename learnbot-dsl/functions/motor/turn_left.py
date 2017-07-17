from __future__ import division, print_function
import time, math


def turn_left(lbot, duration =1, rotSpeed=-0.2,  verbose=False):
	if rotSpeed< -lbot.max_rot:	#lbot.max_rot set as the maximum possible rotational speed of the Learnbot
		lbot.rot= -lbot.max_rot
	else:
		lbot.rot= rotSpeed

	lbot.setRobotSpeed(lbot.adv, lbot.rot)

	if verbose:	
		print('~ Learnbot turning left ...')

	if duration != 0:	# The bot continues to turn right for the given duration
		time.sleep(duration)

	lbot.setRobotSpeed(0, 0)	# The bot setRobotSpeed