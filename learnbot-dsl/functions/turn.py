import time
def turn(lbot, angle=0):
	lbot.setRobotSpeed(lbot.adv, float(angle*3.14/180))
	time.sleep(1)
	print('~ Learnbot has turned by ' + str(angle) + ' degrees')