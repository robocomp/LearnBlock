def obstaculo_frontal(lbot, threshold= 150, verbose=False):
	sonarsValue = lbot.getSonars()
	if sonarsValue['front'] < threshold:
		lbot.publish_topic("obstaculo_frontal")
		if verbose:
			print('Obstacle in front of Learnbot')
		return True
	if verbose:
		print('No obstacle in front of Learnbot')
	return False
