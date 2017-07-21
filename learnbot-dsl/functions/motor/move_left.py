from __future__ import print_function
from functions import *


def move_left(lbot, params, verbose=False):
	def_params=[0,20,-0.2]
	assert len(params)<=len(def_params),('bad params in move_left [duration,advSpeed,rotSpeed]',len(params))
	if len(params)<len(def_params):
		t= len(params)
		while t<len(def_params):
			params.append(def_params[t])
			t=t+1

	duration,advSpeed,rotSpeed= params
	functions.get("move_straight")(lbot, [0, advSpeed], verbose)
	functions.get("turn_left")(lbot, [duration, rotSpeed], verbose)

