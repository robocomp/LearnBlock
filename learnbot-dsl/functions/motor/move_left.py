from __future__ import print_function
from functions import *


def move_left(lbot, duration=0, advSpeed=20, rotSpeed=-0.2, verbose=False):
	functions.get("move_straight")(lbot, 0, advSpeed, verbose)
	functions.get("turn_left")(lbot, duration, rotSpeed, verbose)

