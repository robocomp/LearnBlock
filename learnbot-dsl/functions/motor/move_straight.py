from functions import *
import time


def move_straight(lbot, duration=0, verbose=False):
	if lbot.adv <= 0:
		lbot.adv= 40	#Default value

	lbot.rot= 0			#Setting rotation to zero
	lbot.setRobotSpeed(lbot.adv, lbot.rot)

	if verbose:
		print('~ Learnbot moving straight ...')
	if duration != 0:	# 0 means until next command
		time.sleep(duration)
		functions.get("stop_bot")(lbot)
