
def is_moving_left(lbot):
	rot = lbot.getRot()
	adv = lbot.getAdv()
	if rot is not None and adv is not None:
		return rot < 0 and adv > 0
	return False
