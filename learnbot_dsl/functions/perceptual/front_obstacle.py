def front_obstacle(lbot, threshold= 200, verbose=False):
	sonarsValue = lbot.getSonars()[1:4]
	if min(sonarsValue) < threshold:
		if verbose:
			print('Obstacle in front of Learnbot')
		return True
	if verbose:
		print('No obstacle in front of Learnbot')
	return False
