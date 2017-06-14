def get_distance(lbot, params=None, verbose=False):
	sonarsValue = lbot.getSonars()
	if verbose:
		print(sonarsValue)
	return sonarsValue
