import time
def turn_back(lbot):
	lbot.setRobotSpeed(lbot.adv, 3.14)
	time.sleep(1)
	print('~ Learnbot has turned back')