import sys
import cv2
import time
import LearnBotClient
from functions import *

#EXECUTION: python go_to_target_example.py

global lbot
lbot = LearnBotClient.Client(sys.argv)


while True:

	functions.get("get_pose")(lbot, True)
	if functions.get("target_at_front")(lbot, -100, 500, 0.2, True):
		print "Target at front"

