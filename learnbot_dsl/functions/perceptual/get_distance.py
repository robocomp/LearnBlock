def get_distance(lbot, verbose=False):
	sonarsValue = lbot.getSonars()
	if verbose:
		print(sonarsValue)
	return sonarsValue
