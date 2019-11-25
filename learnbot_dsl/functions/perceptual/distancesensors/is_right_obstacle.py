def is_right_obstacle(lbot, threshold= 200):
	distanceValues = lbot.getDistanceSensors()
	if distanceValues == None:
		return False
	if min(distanceValues["right"]) < threshold:
		return True
	return False
