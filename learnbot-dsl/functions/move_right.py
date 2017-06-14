from functions import *
def move_right(lbot, duration= 0):
	functions.get("turn_right")(lbot)
	functions.get("move_straight")(lbot, duration)
		
