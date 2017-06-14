from functions import *
from __future__ import print_function

def move_left(lbot, params=None):
	assert len(params) is not None, ('bad params in move_left [duration]',len(params))
	duration = params[0]
	functions.get("turn_left")(lbot)
	functions.get("move_straight")(lbot, duration)
