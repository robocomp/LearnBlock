def is_front_obstacle(lbot, threshold= 200):
	distanceValues = lbot.getDistanceSensors()["front"]
	if distanceValues == None:
		return False
	if min(distanceValues) < threshold:
		return True
	return False
