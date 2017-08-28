import sys
import cv2
import time
import LearnBotClient
from functions import *

#EXECUTION: python wander_example.py

global lbot
lbot = LearnBotClient.Client(sys.argv)


while True:

	if functions.get("obstacle_free")(lbot):
		functions.get("move_straight")(lbot,0,100)
	else:
		functions.get("turn_right")(lbot,0,0.4)

