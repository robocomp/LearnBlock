from __future__ import print_function, absolute_import
import numpy
import time


def slow_down(lbot, decAdv=-0.2, decRot=-0.11):
	currAdv = lbot.getAdv()
	currRot = lbot.getRot()
	if currAdv is not None and currRot is not None:
		aR = numpy.sign(currRot)

		adv = currAdv * aR + decAdv
		if aR != numpy.sign(adv):
			adv = 0

		sR = numpy.sign(currRot)
		rot = lbot.getRot() + decRot * sR
		if sR!=numpy.sign(rot):
			rot = 0
		lbot.setBaseSpeed(adv, rot)
		time.sleep(0.1)
