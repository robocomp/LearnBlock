from __future__ import print_function


def set_move(lbot, params):
	def_params=[0,0]
	assert len(params)<=len(def_params),('bad params in set_move [vRot, vAdv]',len(params))
	if len(params)<len(def_params):
		t= len(params)
		while t<len(def_params):
			params.append(def_params[t])
			t=t+1

	lbot.adv, lbot.rot = params
	lbot.setRobotSpeed(lbot.adv, lbot.rot)
