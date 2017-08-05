"""
This is automatically generated python script
Author: aniq55 (C) 2017, for RoboComp Learnbot
Generated on: Sat Aug  5 13:28:51 2017
"""

import sys
import cv2
import LearnBotClient
from functions import *
import time
global lbot
lbot = LearnBotClient.Client(sys.argv)
lbot.adv, lbot.rot= 0,0
activationList={}
activationList['init']=False
activationList['start_following_black']=False
activationList['continue_following_black']=False
activationList['follow_black']=False
activationList['start_following_red']=False
activationList['continue_following_red']=False
activationList['follow_red']=False
if activationList['init'] :
	activationList['start_following_black']=True
	activationList['init']=False
if activationList['start_following_black'] :
	activationList['follow_black']=True
	if not functions.get("line_crossing")(lbot) :
		activationList['start_following_black']=False
if activationList['continue_following_black'] :
	if functions.get("line_crossing")(lbot) :
		activationList['follow_black']=False
		activationList['continue_following_black']=False
if activationList['follow_black'] :
	if functions.get("center_black_line")(lbot) :
		functions.get("move_straight")(lbot)
	elif functions.get("right_black_line")(lbot) :
		functions.get("move_right")(lbot)
	elif functions.get("left_black_line")(lbot) :
		functions.get("move_left")(lbot)
	else:
		functions.get("slow_down")(lbot)
if activationList['start_following_red'] :
	activationList['follow_red']=True
	if not functions.get("line_crossing")(lbot) :
		activationList['start_following_red']=False
if activationList['continue_following_red'] :
	if functions.get("line_crossing")(lbot) :
		activationList['follow_red']=False
		activationList['continue_following_red']=False
if activationList['follow_red'] :
	if functions.get("center_red_line")(lbot) :
		functions.get("move_straight")(lbot)
	elif functions.get("right_red_line")(lbot) :
		functions.get("move_right")(lbot)
	elif functions.get("left_red_line")(lbot) :
		functions.get("move_left")(lbot)
	else:
		functions.get("slow_down")(lbot)

