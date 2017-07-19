from __future__ import print_function
import math as m

def target_at_front(lbot, targetX, targetY, maxFrontAngle = 0.2, verbose=False):
	x, y, alpha = lbot.getPose()
	targetFromRobotX = m.cos(alpha)*(targetX-x) - m.sin(alpha)*(targetY-y)
	targetFromRobotY = m.sin(alpha)*(targetX-x) + m.cos(alpha)*(targetY-y)
	frontAngle = m.atan2(targetFromRobotX, targetFromRobotY)
	if verbose:
		print("Target from robot", targetFromRobotX, targetFromRobotY)
	if frontAngle<=maxFrontAngle:
		return True
	return False

