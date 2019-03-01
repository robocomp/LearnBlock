def front_obstacle(lbot, threshold= 200, verbose=False):
	sonarsValue = lbot.getSonars()["front"]
	if sonarsValue == None:
		return False
	if min(sonarsValue) < threshold:
		if verbose:
			print('Obstacle in front of Learnbot')
		return True
	if verbose:
		print('No obstacle in front of Learnbot')
	return False
