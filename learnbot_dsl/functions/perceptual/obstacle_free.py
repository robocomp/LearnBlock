def obstacle_free(lbot, threshold= 200, verbose=False):
	sonarsValue = lbot.getSonars()
	if min(sonarsValue) > threshold:
		if verbose:
			print('No obstacles around Learnbot')
		return True
	if verbose:
		print('Learnbot is not obstacle free')
	return False
