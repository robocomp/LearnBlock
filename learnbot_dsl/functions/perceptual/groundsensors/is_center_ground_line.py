from __future__ import print_function, absolute_import

def is_center_ground_line(lbot):
	gsensors = lbot.getGroundSensors()
	if gsensors is not None and gsensors["left"] is not None and gsensors["right"] is not None:
		if gsensors["central"] is not None:
			return gsensors["central"]<50
		else:
			return gsensors["left"]<50 and gsensors["right"]<50
	return False
