def is_front_obstacle(lbot, threshold= 200):
	sonarsValue = lbot.getSonars()["front"]
	if sonarsValue == None:
		return False
	if min(sonarsValue) < threshold:
		return True
	return False
