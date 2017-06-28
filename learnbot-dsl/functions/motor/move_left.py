from __future__ import print_function
from functions import *


def move_left(lbot, duration=0):
	functions.get("turn_left")(lbot)
	functions.get("move_straight")(lbot, duration)
