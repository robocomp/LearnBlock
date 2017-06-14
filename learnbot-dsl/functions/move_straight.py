from functions import *
import time

def move_straight(lbot, params=None, verbose=False):
	assert len(params) is not None, ('bad params in move_straight [duration,[max_speed=100]]',len(params))

	duration = params[0]
	try:
		max_speed = params[1]
	except:
		max_speed = 100
	lbot.adv = max_speed if (lbot.adv == 0) else lbot.adv
	lbot.setRobotSpeed(lbot.adv, 0)
	if verbose:
		print('~ Learnbot moving straight ...')
	if duration != 0:	# 0 means until next command
		time.sleep(duration)
		functions.get("stop_bot")(lbot)
