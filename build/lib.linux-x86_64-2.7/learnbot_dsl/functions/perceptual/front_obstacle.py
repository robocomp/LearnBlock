def front_obstacle(lbot, threshold= 200, verbose=False):
	sonarsValue = lbot.getSonars()
	if sonarsValue['front'] < threshold:
		lbot.publish_topic("front_obstacle")
		if verbose:
			print('Obstacle in front of Learnbot')
		return True
	if verbose:
		print('No obstacle in front of Learnbot')
	return False
