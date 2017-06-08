import sys
import LearnBotClient

class LearnbotCode(LearnBotClient.Client):
	def __init__(self):
		pass

	def set_move(self, params):
		assert len(params) == 2, ('bad params in move robot',len(params))
		vAdv, vRot = params
		self.setRobotSpeed(vAdv, vRot)

	def code(self):
		params = [2,2]
		self.set_move(params)

miclase = LearnbotCode()
miclase.main(sys.argv)
