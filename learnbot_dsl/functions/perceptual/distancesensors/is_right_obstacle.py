def is_right_obstacle(lbot, threshold= 200):
	sonarsValue = lbot.getSonars()["right"]
	if min(sonarsValue) < threshold:
		return True
	return False
