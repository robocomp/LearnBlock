import sys, time
import cv2
import LearnBotClient_PhysicalRobot as LearnBotClient
from functions import *

#EXECUTION: python code_example.py Ice.Config=config

global lbot
lbot = LearnBotClient.Client(sys.argv)

i=0
while i<1500:
	func1 = functions.get("get_distance")
	usList = func1(lbot)
	print usList
	image = lbot.getImage()
	image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
	cv2.namedWindow("im")
	cv2.imshow("im",image)
	keypress=cv2.waitKey(1)
	if keypress & 0xFF == 113: 
		i=1500
	time.sleep(0.066)
	i = i+1

print functions.get("obstacle_free")(lbot)

centerLine = functions.get("center_black_line")(lbot)

if centerLine:
	print "go ahead"
else:
	print "turn"

#while functions.get("get_distance")(lbot)["front"]>100:
#	functions.get("set_move")(lbot, [50,0])
	
#functions.get("set_move")(lbot, [0,0])

