from __future__ import print_function
def subscribe(lbot,robotId, timeWait = 5):
	msg = lbot.subscribe_topic("Robot " + str(robotId),timeWait)
	print msg
	return msg
