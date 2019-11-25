def is_left_obstacle(lbot, threshold = 200):
	distanceValues = lbot.getDistanceSensors()
	if distanceValues == None:
		return False
	if min(distanceValues["left"]) < threshold:
		return True
	return False
