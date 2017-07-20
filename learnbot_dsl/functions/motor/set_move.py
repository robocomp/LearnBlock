from __future__ import print_function


def set_move(lbot, params):
	assert len(params) == 2, ('bad params in move robot [vRot, vAdv]',len(params))
	lbot.adv, lbot.rot = params
	lbot.setRobotSpeed(lbot.adv, lbot.rot)
