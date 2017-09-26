from __future__ import print_function
import time
def move_left(lbot, duration=0.05, advSpeed=20, rotSpeed=-0.3, verbose=False):
	lbot.setRobotSpeed(advSpeed, rotSpeed)
	if duration != 0:
		time.sleep(duration)

