def stop_bot(lbot, params=None):
	lbot.adv, lbot.rot= 0,0
	lbot.setRobotSpeed(lbot.adv, lbot.rot)
	print('~ Learnbot stopped')
