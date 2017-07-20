import sys
import cv2
import time
import LearnBotClient
from functions import *

#EXECUTION: python code_example.py Ice.Config=config

global lbot
lbot = LearnBotClient.Client(sys.argv)


while True:

	if functions.get("line_crossing")(lbot):
		print "LINE CROSSING!!!"


	if functions.get("center_red_line")(lbot):
		functions.get("move_straight")(lbot)
		print "go ahead"
	elif functions.get("right_red_line")(lbot):
		functions.get("move_right")(lbot)
		print "turn right"
	elif functions.get("left_red_line")(lbot):
		functions.get("move_left")(lbot)
		print "turn left"
	else:
		functions.get("slow_down")(lbot)
		print "slow_down"

