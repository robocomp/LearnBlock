def is_front_obstacle(lbot, threshold= 200):
	distanceValues = lbot.getDistanceSensors()
	if distanceValues == None:
		return False
	if min(distanceValues["front"]) < threshold:
		return True
	return False
