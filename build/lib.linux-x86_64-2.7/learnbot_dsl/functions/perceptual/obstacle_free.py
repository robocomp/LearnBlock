def obstacle_free(lbot, threshold= 200, verbose=False):
	sonarsValue = lbot.getSonars()
	f= sonarsValue['front'] > threshold
	b= sonarsValue['back'] > threshold
	r= sonarsValue['right'] > threshold
	l= sonarsValue['left'] > threshold

	if f and r and l:
		lbot.publish_topic("obstacle_free")
		if verbose:
			print('No obstacles around Learnbot')
		return True
	if verbose:
		print('Learnbot is not obstacle free')
	return False
