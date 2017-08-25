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

while True:
	# functions.get("move_straight")(lbot)
	# functions.get("get_")(lbot)
	functions.get("follow_line")(lbot)