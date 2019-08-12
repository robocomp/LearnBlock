def is_left_obstacle(lbot, threshold = 200):
	sonarsValue = lbot.getSonars()["left"]
	if min(sonarsValue) < threshold:
		return True
	return False
