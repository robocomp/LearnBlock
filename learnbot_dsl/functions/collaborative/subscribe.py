def subscribe(lbot,robotId,timeWait):
	print ("Inside functions : subscribe")
	msg = lbot.subscribe_topic("Robot " + str(robotId),timeWait)
	print msg
	return msg
