def right_obstacle(lbot, threshold= 200, verbose=False):
	sonarsValue = lbot.getSonars()["right"]
	if min(sonarsValue) < threshold:
		if verbose:
			print('Obstacle right of Learnbot')
		return True
	if verbose:
		print('No obstacle right of Learnbot')
	return False
