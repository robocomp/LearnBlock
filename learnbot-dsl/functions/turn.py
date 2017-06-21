import time
#To make it compatible with python 3
from __future__ import print_function


def turn(lbot, params=None, verbose=False):
	assert len(params) is not None, ('bad params in move_straight [angle,[format_angle='+r"'degrees'"+']]',len(params))
	angle = params[0]
	try:
		format_angle = params[1]
	except:
		format_angle = 'radians'
	if (format_angle == 'degrees'):
		lbot.setRobotSpeed(lbot.adv, math.radians(angle))
	else:
		lbot.setRobotSpeed(lbot.adv, angle)
	time.sleep(1)
	if verbose:
		print('~ Learnbot has turned by ' + str(angle) + ' degrees')