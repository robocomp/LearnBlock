from __future__ import print_function


def mover(lbot, adv, rot):
	lbot.adv, lbot.rot = adv,rot
	lbot.setRobotSpeed(lbot.adv, lbot.rot)
