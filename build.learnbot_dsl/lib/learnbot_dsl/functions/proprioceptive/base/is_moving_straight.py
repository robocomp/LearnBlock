
def is_moving_straight(lbot):
	return lbot.getRot() is 0 and lbot.getAdv() > 0
