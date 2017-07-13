from __future__ import print_function
import numpy


def slow_down(lbot, decAdv=-0.1, decRot=-0.01):
	lbot.adv = lbot.adv + decAdv
	if lbot.adv<0:
		lbot.adv=0

	sR = numpy.sign(lbot.rot)
	lbot.rot = lbot.rot + decRot*sR
	if sR!=numpy.sign(lbot.rot):
		lbot.rot=0
		
	lbot.setRobotSpeed(lbot.adv, lbot.rot)
