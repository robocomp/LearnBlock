from functions import *
import time


def move_straight(lbot, duration=0, advSpeed=40, verbose=False):
	max_speed=advSpeed
	lbot.adv = max_speed if (lbot.adv == 0) else lbot.adv
	lbot.setRobotSpeed(lbot.adv, 0)
	if verbose:
		print('~ Learnbot moving straight ...')
	if duration != 0:	# 0 means until next command
		time.sleep(duration)
		functions.get("stop_bot")(lbot)
