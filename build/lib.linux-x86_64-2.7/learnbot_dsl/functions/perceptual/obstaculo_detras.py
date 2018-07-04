def obstaculo_detras(lbot, threshold= 200, verbose=False):
	sonarsValue = lbot.getSonars()
	if sonarsValue['back'] < threshold:
		lbot.publish_topic("obstaculo_detras")
		if verbose:
			print('Obstacle behind Learnbot')
		return True
	if verbose:
		print('No obstacle behind Learnbot')
	return False
