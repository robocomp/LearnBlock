def is_back_obstacle(lbot, threshold= 200):
	sonarsValue = lbot.getSonars()
	if sonarsValue['back'] < threshold:
		return True
	return False
