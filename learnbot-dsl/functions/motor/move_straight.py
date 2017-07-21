from functions import *
import time


def move_straight(lbot, params, verbose=False):
	def_params=[0,40]
	assert len(params)<=len(def_params),('bad params in set_move [vRot, vAdv]',len(params))
	if len(params)<len(def_params):
		t= len(params)
		while t<len(def_params):
			params.append(def_params[t])
			t=t+1

	duration, advSpeed= params
	lbot.setRobotSpeed(advSpeed, 0)
	if verbose:
		print('~ Learnbot moving straight ...')
	if duration != 0:	# 0 means until next command
		time.sleep(duration)
		functions.get("stop_bot")(lbot)
