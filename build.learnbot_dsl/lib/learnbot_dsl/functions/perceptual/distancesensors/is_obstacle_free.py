def is_obstacle_free(lbot, threshold = 200):
	sonarsvalue = lbot.getSonars()
	values = sonarsvalue["front"]
	values += sonarsvalue["left"]
	values += sonarsvalue["right"]
	if min(values) < threshold:
		return False
	return True
