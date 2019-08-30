def is_left_obstacle(lbot, threshold = 200):
	distanceValues = lbot.getDistanceSensors()["left"]
	if min(distanceValues) < threshold:
		return True
	return False
