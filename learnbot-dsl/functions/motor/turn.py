from __future__ import print_function
import time, math

def turn(lbot, params, verbose=False):
	def_params=[0]
	assert len(params)<=len(def_params),('bad params in set_move [vRot, vAdv]',len(params))
	if len(params)<len(def_params):
		t= len(params)
		while t<len(def_params):
			params.append(def_params[t])
			t=t+1
	angle,= params
	lbot.setRobotSpeed(lbot.adv, math.radians(angle))
	time.sleep(1)
	if verbose:
		print('~ Learnbot has turned by ' + str(angle) + ' degrees')