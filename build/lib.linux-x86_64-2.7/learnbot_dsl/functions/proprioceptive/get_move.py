from __future__ import print_function

def get_move(lbot, params=None):
	lbot.publish_topic("get_move")
	print("The advance speed is" + "{:4.2f}".format(lbot.adv) + \
		", the angular speed is "+ "{:1.4f}".format(lbot.rot))
