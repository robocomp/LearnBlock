import sys
import cv2
import LearnBotClient
from functions import *

#EXECUTION: python code_example.py Ice.Config=config

global lbot
lbot = LearnBotClient.Client(sys.argv)

for f in functions:
	print f

func1 = functions.get("get_distance")
usList = func1(lbot)
print usList

print functions.get("obstacle_free")(lbot)

#while functions.get("get_distance")(lbot)["front"]>100:
#	functions.get("set_move")(lbot, [50,0])
	
#functions.get("set_move")(lbot, [0,0])

