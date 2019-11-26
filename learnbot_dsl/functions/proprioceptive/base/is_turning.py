
def is_turning(lbot):
	rot = lbot.getRot()
	adv = lbot.getAdv()
	if rot is not None and adv is not None:
		return rot is not 0 and adv is 0
	return False
