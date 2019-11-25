def is_obstacle_free(lbot, threshold = 200):
	distanceValues = lbot.getDistanceSensors()
	if distanceValues == None:
		return False
	values = []
	values += distanceValues["front"]
	values += distanceValues["left"]
	values += distanceValues["right"]
	if min(values) < threshold:
		return False
	return True
