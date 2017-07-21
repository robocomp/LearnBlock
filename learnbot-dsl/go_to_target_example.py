import sys
import cv2
import time
import LearnBotClient
from functions import *

#EXECUTION: python go_to_target_example.py

global lbot
lbot = LearnBotClient.Client(sys.argv)

targetX = 0
targetY = 1800

while not functions.get("near_to_target")(lbot, targetX, targetY):

	functions.get("get_pose")(lbot, True)

	if not functions.get("obstacle_free")(lbot, 400):

		if functions.get("front_obstacle")(lbot):
			if functions.get("left_obstacle")(lbot):
				functions.get("turn_right")(lbot)
				print "avoiding: turning right"
			else:
				functions.get("turn_left")(lbot)
				print "avoiding: turning left"
		else:
			if functions.get("left_obstacle")(lbot):
				functions.get("move_right")(lbot)
				print "avoiding: moving right"
			elif functions.get("right_obstacle")(lbot):
				functions.get("move_left")(lbot)
				print "avoiding: moving left"
			else:
				functions.get("move_straight")(lbot)
				print "avoiding: moving straight"
	else:
		if functions.get("target_at_front")(lbot, targetX, targetY):
			functions.get("move_straight")(lbot)
			print "going to target"
		elif functions.get("target_at_right")(lbot, targetX, targetY):
			print "target at right"
			functions.get("move_right")(lbot)
		else:
			print "target at left"
			functions.get("move_left")(lbot)

	time.sleep(0.1)

functions.get("stop_bot")(lbot)
exit(0)
