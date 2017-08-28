def get_pose(lbot, verbose=False):
	x, y, alpha = lbot.getPose()
	if verbose:
		print('Robot pose:', x, y, alpha)
	return x, y, alpha
