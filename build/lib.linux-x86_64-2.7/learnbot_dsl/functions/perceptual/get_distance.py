def get_distance(lbot, verbose=False):
	sonarsValue = lbot.getSonars()
	lbot.publish_topic("get_distance")
	if verbose:
		print(sonarsValue)
	return sonarsValue
