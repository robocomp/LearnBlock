#To make it compatible with python 3
from __future__ import print_function

def get_move(lbot, params=None):
	print("The advance speed is" + "{:4.2f}".format(lbot.adv) + \
		", the angular speed is "+ "{:1.4f}".format(lbot.rot))