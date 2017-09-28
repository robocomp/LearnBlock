from __future__ import division, print_function
import time, math

def girar_izquierda(lbot, duration=0.05, rotSpeed=-0.3, verbose=False):
	lbot.setRobotSpeed(0, rotSpeed)
	if verbose:
		print('~ Learnbot turning left ...')
	if duration != 0:
		time.sleep(duration)
		#lbot.setRobotSpeed(0, 0)

