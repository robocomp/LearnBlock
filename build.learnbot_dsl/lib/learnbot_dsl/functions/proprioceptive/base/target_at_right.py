import math as m

def target_at_right(lbot, targetX, targetY):
	x, y, alpha = lbot.getPose()
	targetFromRobotX = m.cos(alpha)*(targetX-x) - m.sin(alpha)*(targetY-y)
	if targetFromRobotX > 0:
		return True
	return False

