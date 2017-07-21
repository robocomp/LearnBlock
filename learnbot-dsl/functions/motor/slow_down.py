from __future__ import print_function
import numpy
import time


def slow_down(lbot, params):
	def_params=[0.15,-0.2,-0.001]
	assert len(params)<=len(def_params),('bad params in slow_down [duration,decAdv,decRot]',len(params))
	if len(params)<len(def_params):
		t= len(params)
		while t<len(def_params):
			params.append(def_params[t])
			t=t+1

	duration,decAdv,decRot= params
	lbot.adv = lbot.adv + decAdv
	if lbot.adv<0:
		lbot.adv=0

	sR = numpy.sign(lbot.rot)
	lbot.rot = lbot.rot + decRot*sR
	if sR!=numpy.sign(lbot.rot):
		lbot.rot=0
	
	lbot.setRobotSpeed(lbot.adv, lbot.rot)

	if duration!=0:
		time.sleep(duration)
