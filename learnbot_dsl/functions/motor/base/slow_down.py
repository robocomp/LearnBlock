from __future__ import print_function, absolute_import
import numpy
import time


def slow_down(lbot, duration=0.15, decAdv=-2, decRot=-0.02):
	adv = lbot.getAdv() + decAdv
	if adv<0:
		adv=0

	sR = numpy.sign(lbot.getRot())
	rot = lbot.getRot() + decRot*sR
	if sR!=numpy.sign(rot):
		rot=0
	
	lbot.setBaseSpeed(adv, rot)

	if duration!=0:
		time.sleep(duration)
