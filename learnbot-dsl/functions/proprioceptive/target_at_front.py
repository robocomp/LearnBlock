from __future__ import print_function
import math as m

def target_at_front(lbot, targetX, targetY, diffTargetX = 20, verbose=False):
	x, y, alpha = lbot.getPose()
	targetFromRobotX = m.cos(alpha)*(targetX-x) - m.sin(alpha)*(targetY-y)
	targetFromRobotY = m.sin(alpha)*(targetX-x) + m.cos(alpha)*(targetY-y)
	if verbose:
		print("Target from robot", targetFromRobotX, targetFromRobotY)
	if targetFromRobotY>=0 and m.fabs(targetFromRobotX)<=diffTargetX:
		return True
	return False

