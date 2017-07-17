from functions import *

def move_left(lbot, duration=0, verbose=False):
	functions.get("turn_left")(lbot, verbose)
	functions.get("move_straight")(lbot, duration, verbose)

