import sys
import cv2
import LearnBotClient
from functions import *
import time

global lbot
lbot = LearnBotClient.Client(sys.argv)

# To keep track of the speed of Learnbot
lbot.adv, lbot.rot= 0,0

#####################
#	 CODE BEGINS	#
#####################


print(functions.get("front_obstacle")(lbot,2000))
print(functions.get("back_obstacle")(lbot,2000, True))
print(functions.get("right_obstacle")(lbot,2000))
print(functions.get("left_obstacle")(lbot,2000))

print(functions.get("obstacle_free")(lbot))
print(functions.get("obstacle_free")(lbot,2000, True))
print(functions.get("obstacle_free")(lbot,200, True))

print(functions.get("front_obstacle")(lbot))
print(functions.get("back_obstacle")(lbot))
print(functions.get("right_obstacle")(lbot))
print(functions.get("left_obstacle")(lbot))
