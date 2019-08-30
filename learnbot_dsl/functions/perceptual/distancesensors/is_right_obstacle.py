def is_right_obstacle(lbot, threshold= 200):
	distanceValues = lbot.getDistanceSensors()["right"]
	if min(distanceValues) < threshold:
		return True
	return False
