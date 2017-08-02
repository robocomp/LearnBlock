def back_obstacle(lbot, threshold= 200, verbose=False):
	sonarsValue = lbot.getSonars()
	if sonarsValue['back'] < threshold:
		if verbose:
			print('Obstacle behind Learnbot')
		return True
	if verbose:
		print('No obstacle behind Learnbot')
	return False
