from functions import *


def move_right(lbot, duration=0, advSpeed=20, rotSpeed=0.2, verbose=False):
	functions.get("move_straight")(lbot, 0, advSpeed, verbose)
	functions.get("turn_right")(lbot,duration, rotSpeed, verbose)

