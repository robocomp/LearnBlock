def get_distance(lbot, left=0, front=1, right=0,verbose=False):
	sonarsValue = lbot.getSonars()
	if verbose:
		print(sonarsValue)
	if left:
		return min(sonarsValue[:2])
	elif front:
		return min(sonarsValue[1:4])
	elif right:
		return min(sonarsValue[3:])
	else:
		return min(sonarsValue[1:4])