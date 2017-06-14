from functions import *
import time
def move_straight(lbot, duration= 0):
	if lbot.adv == 0:
		lbot.adv = 100
	print('~ Learnbot moving straight ...')
	lbot.setRobotSpeed(lbot.adv, 0)
	if duration!=0:	# 0 means until next command
		time.sleep(duration)
		functions.get("stop_bot")(lbot)
