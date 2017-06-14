from functions import *
def move_right(lbot, params=None, verbose=False):
	assert len(params) is not None, ('bad params in move_straight [duration]',len(params))
	duration=params[0]
	functions.get("turn_right")(lbot)
	functions.get("move_straight")(lbot, duration)