from __future__ import print_function
import math as m

def target_at_right(lbot, targetX, targetY, verbose=False):
	x, y, alpha = lbot.getPose()
	targetFromRobotX = m.cos(alpha)*(targetX-x) - m.sin(alpha)*(targetY-y)
	targetFromRobotY = m.sin(alpha)*(targetX-x) + m.cos(alpha)*(targetY-y)
	if verbose:
		print("Target from robot", targetFromRobotX, targetFromRobotY)
	if targetFromRobotX>0:
		lbot.publish_topic("target_at_right")
		return True
	return False

