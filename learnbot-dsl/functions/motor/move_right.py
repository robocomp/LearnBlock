from functions import *

def move_right(lbot, duration=0, verbose=False):
	functions.get("move_straight")(lbot, duration, verbose)
	functions.get("turn_right")(lbot, verbose)

