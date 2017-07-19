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

	if functions.get("front_obstacle")(lbot):
		while functions.get("front_obstacle")(lbot) or not functions.get("left_obstacle")(lbot, 400):
			functions.get("turn_right")(lbot)
		print "front obstacle"
	else:
		if functions.get("target_at_front")(lbot, targetX, targetY):
			functions.get("move_straight")(lbot)
			print "going to target"
		elif functions.get("target_at_right")(lbot, targetX, targetY):
			print "target at right"
			if functions.get("right_obstacle")(lbot, 400):
				functions.get("move_left")(lbot)
			else:
				functions.get("turn_right")(lbot)
		else:

			if functions.get("left_obstacle")(lbot, 400):
				print "target at left: move straight"
				functions.get("move_right")(lbot)
			else:
				print "target at left: turn left"
				functions.get("turn_left")(lbot)

functions.get("stop_bot")(lbot)
