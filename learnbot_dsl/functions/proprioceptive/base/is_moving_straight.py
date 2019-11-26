
def is_moving_straight(lbot):
	rot = lbot.getRot()
	adv = lbot.getAdv()
	if rot is not None and adv is not None:
		return rot is 0 and adv > 0
	return False
