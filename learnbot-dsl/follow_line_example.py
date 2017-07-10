import sys
import cv2
import time
import LearnBotClient
from functions import *

#EXECUTION: python code_example.py Ice.Config=config

global lbot
lbot = LearnBotClient.Client(sys.argv)


while True:

	centerLine = functions.get("center_black_line")(lbot)
	leftLine = functions.get("left_black_line")(lbot)
	rightLine = functions.get("right_black_line")(lbot)

	if centerLine:
		functions.get("set_move")(lbot,[40, 0])
		print "go ahead"
	elif rightLine:
		functions.get("set_move")(lbot,[20, 0.2])
		print "turn right"
	elif leftLine:
		functions.get("set_move")(lbot,[20, -0.2])
		print "turn left"
	else:
		functions.get("stop_bot")(lbot)
		print "stop"

	time.sleep(0.15) 
