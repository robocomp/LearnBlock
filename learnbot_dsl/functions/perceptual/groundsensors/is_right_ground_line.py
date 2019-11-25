from __future__ import print_function, absolute_import

def is_right_ground_line(lbot):
	gsensors = lbot.getGroundSensors()
	if gsensors is not None and gsensors["left"] is not None and gsensors["right"] is not None:
		return gsensors["left"]>50 and gsensors["right"]<50
	return False
