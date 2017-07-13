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
		functions.get("set_move")(lbot,[40, 0])
		print "go ahead"
	elif functions.get("right_red_line")(lbot):
		functions.get("set_move")(lbot,[20, 0.1])
		print "turn right"
	elif functions.get("left_red_line")(lbot):
		functions.get("set_move")(lbot,[20, -0.1])
		print "turn left"
	else:
		functions.get("stop_bot")(lbot)
		print "stop"

	time.sleep(0.15) 
