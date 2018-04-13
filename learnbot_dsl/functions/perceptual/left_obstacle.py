def left_obstacle(lbot, threshold= 200, verbose=False):
	sonarsValue = lbot.getSonars()[:2]
	if min(sonarsValue) < threshold:
		if verbose:
			print('Obstacle left of Learnbot')
		return True
	if verbose:
		print('No obstacle left of Learnbot')
	return False
