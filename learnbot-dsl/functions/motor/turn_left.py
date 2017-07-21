from __future__ import division, print_function
import time, math

def turn_left(lbot, params, verbose=False):
	def_params=[0,-0.2]
	assert len(params)<=len(def_params),('bad params in turn_left [duration,rotSpeed]',len(params))
	if len(params)<len(def_params):
		t= len(params)
		while t<len(def_params):
			params.append(def_params[t])
			t=t+1

	duration, rotSpeed= params
	lbot.setRobotSpeed(lbot.adv, rotSpeed)
	if verbose:
		print('~ Learnbot turning left ...')
	if duration != 0:
		time.sleep(duration)
		lbot.setRobotSpeed(0, 0)

