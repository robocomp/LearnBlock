from functions import *

def move_right(lbot, duration=0, verbose=False):
	functions.get("turn_right")(lbot, verbose)
	functions.get("move_straight")(lbot, duration, verbose)

