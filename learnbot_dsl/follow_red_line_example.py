import sys
import cv2
import time
import LearnBotClient_PhysicalRobot as LearnBotClient
from functions import *

#EXECUTION: python code_example.py

global lbot
lbot = LearnBotClient.Client(sys.argv)

LL_red = (0, 70, 50)
LU_red = (10, 255, 255)

finish = False
#while True:
while not finish:

	#if functions.get("line_crossing")(lbot):
	#	print "LINE CROSSING!!!"


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

	image = lbot.getImage()
	image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
	cv2.namedWindow("im")
	cv2.imshow("im",image)
	keypress=cv2.waitKey(1)
	if keypress & 0xFF == 113: 
		finish = True
		functions.get("stop_bot")(lbot)

#	time.sleep(0.1)

