def is_back_obstacle(lbot, threshold= 200):
	distanceValues = lbot.getDistanceSensors()
	if distanceValues['back'] < threshold:
		return True
	return False
