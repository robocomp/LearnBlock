import os
def obstacle_free(lbot, threshold = 200, verbose=False):
	sonarsvalue = lbot.getSonars()
	values = sonarsvalue["front"]
	values += sonarsvalue["left"]
	values += sonarsvalue["right"]
	if min(values) < threshold:
		if verbose:
			print('No obstacles around Learnbot')
		return True
	if verbose:
		print('Learnbot is not obstacle free')
	return False
