from __future__ import print_function, absolute_import
import time
def move_left(lbot, duration=0.05, advSpeed=20, rotSpeed=-0.25, verbose=False):
	lbot.setBaseSpeed(advSpeed, rotSpeed)
	if duration != 0:
		time.sleep(duration)

