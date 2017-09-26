import time


def move_straight(lbot, duration=0.05, advSpeed=40, verbose=False):
	lbot.setRobotSpeed(advSpeed, 0)
	if verbose:
		print('~ Learnbot moving straight ...')
	if duration != 0:	# 0 means until next command
		time.sleep(duration)

