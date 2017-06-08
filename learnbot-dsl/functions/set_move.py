def set_move(self, params):
	assert len(params) == 2, ('bad params in move robot [vRot, vAdv]',len(params))
	vAdv, vRot = params
	self.setRobotSpeed(vAdv, vRot)