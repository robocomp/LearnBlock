import math as m

def target_at_front(lbot, targetX, targetY, diffTargetX = 20):
	x, y, alpha = lbot.getPose()
	targetFromRobotX = m.cos(alpha)*(targetX-x) - m.sin(alpha)*(targetY-y)
	targetFromRobotY = m.sin(alpha)*(targetX-x) + m.cos(alpha)*(targetY-y)
	if targetFromRobotY>=0 and m.fabs(targetFromRobotX)<=diffTargetX:
		return True
	return False

