def get_pose(lbot, verbose=False):
	x, y, alpha = lbot.getPose()
	lbot.publish_topic("get_pose")
	if verbose:
		print('Robot pose:', x, y, alpha)
	return x, y, alpha
