
#EXECUTION: python code.py
from __future__ import print_function, absolute_import
import sys, os, time, traceback
sys.path.insert(0, os.path.join(os.getenv('HOME'), ".learnblock", "clients"))
from EBO import Robot
import signal
import sys

usedFunctions = []

try:
	robot = Robot(availableFunctions = usedFunctions)
except Exception as e:
	print("Problems creating a robot instance")
	traceback.print_exc()
	raise(e)


time_global_start = time.time()
def elapsedTime(umbral):
	global time_global_start
	time_global = time.time()-time_global_start
	return time_global > umbral


def signal_handler(sig, frame):
	robot.stop()
	sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

robot.look_floor()
while True:
	if robot.is_obstacle_free(100):
		if robot.is_center_red_line():
			robot.move_straight()
			robot.expressJoy()
		elif robot.is_right_red_line():
			robot.move_right()
			robot.expressJoy()
		elif robot.is_left_red_line():
			robot.move_left()
			robot.expressJoy()
		else:
			robot.slow_down()
			robot.expressSadness()

	else:
		robot.stop_bot()
robot.stop()
sys.exit(0)

