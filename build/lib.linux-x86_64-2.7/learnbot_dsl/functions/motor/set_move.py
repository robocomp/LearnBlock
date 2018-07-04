from __future__ import print_function


def set_move(lbot, adv, rot):
	lbot.adv, lbot.rot = adv,rot
	lbot.setRobotSpeed(lbot.adv, lbot.rot)
	lbot.publish_topic("set_move")
