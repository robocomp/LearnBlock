from __future__ import print_function
import math as m

def near_to_target(lbot, targetX, targetY, nearDist = 50, verbose=False):
	x, y, alpha = lbot.getPose()
	distToTarget = m.sqrt(m.pow(x-targetX, 2) + m.pow(y-targetY, 2))
	if verbose:
		print("Distance to target position", distToTarget)
	if distToTarget<=nearDist:
		return True
	return False

