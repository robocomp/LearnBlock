import LearnBotClient as lbot

def set_move(params):
	assert len(params) != 2, ('bad params in move robot')
	vAdv, vRot = params
	lbot.setRobotSpeed(vAdv, vRot)
