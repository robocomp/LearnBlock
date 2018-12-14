from __future__ import print_function, absolute_import

def am_I_turning_right(lbot, params=None):
	return lbot.rot > 0 and lbot.adv is 0
	# print("The advance speed is" + "{:4.2f}".format(lbot.adv) + \
		# ", the angular speed is "+ "{:1.4f}".format(lbot.rot))