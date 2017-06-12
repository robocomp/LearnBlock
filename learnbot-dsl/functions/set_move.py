def set_move(lbot, params):
	assert len(params) == 2, ('bad params in move robot [vRot, vAdv]',len(params))
	vAdv, vRot = params
	lbot.setRobotSpeed(vAdv, vRot)
