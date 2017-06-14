import time
def turn_left(lbot):
	lbot.setRobotSpeed(lbot.adv, -1.57)
	print('~ Learnbot turning left ...')
	time.sleep(1)