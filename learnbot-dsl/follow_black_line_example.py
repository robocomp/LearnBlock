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


	if functions.get("center_black_line")(lbot):
		functions.get("set_move")(lbot,[40, 0])
		print "go ahead"
	elif functions.get("right_black_line")(lbot):
		functions.get("set_move")(lbot,[20, 0.2])
		print "turn right"
	elif functions.get("left_black_line")(lbot):
		functions.get("set_move")(lbot,[20, -0.2])
		print "turn left"
	else:
		functions.get("slow_down")(lbot)
		print "slow_down"

