def obstaculo_derecha(lbot, threshold= 200, verbose=False):
	sonarsValue = lbot.getSonars()
	if sonarsValue['right'] < threshold:
		lbot.publish_topic("obstaculo_derecha")
		if verbose:
			print('Obstacle right of Learnbot')
		return True
	if verbose:
		print('No obstacle right of Learnbot')
	return False
