"""
This is automatically generated python script
Author: aniq55 (C) 2017, for RoboComp Learnbot
Generated on: Sat Aug 12 18:08:47 2017
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

#Declaring Event Variables
activationList['var1']=True
activationList['follow_red']=False
activationList['follow_black']=False
activationList['always']=True
activationList['var2']=True
activationList['continue_following_black']=False
activationList['init']=True
activationList['start_following_red']=False
activationList['start_following_black']=False
activationList['continue_following_red']=False

def block1():
	if activationList['init'] :
		if functions.get("center_black_line")(lbot) or functions.get("right_black_line")(lbot) or functions.get("left_black_line")(lbot) :
			activationList['start_following_black']=True
			activationList['init']=False
		elif functions.get("center_red_line")(lbot) or functions.get("right_red_line")(lbot) or functions.get("left_red_line")(lbot) :
			activationList['start_following_red']=True
			activationList['init']=False
		else:
			functions.get("turn_right")(lbot)
def block2():
	if activationList['start_following_black'] :
		activationList['follow_black']=True
		if not functions.get("line_crossing")(lbot) :
			activationList['start_following_black']=False
			activationList['continue_following_black']=True
def block3():
	if activationList['continue_following_black'] :
		if functions.get("line_crossing")(lbot) :
			activationList['follow_black']=False
			activationList['continue_following_black']=False
			activationList['start_following_red']=True
def block4():
	if activationList['follow_black'] :
		if functions.get("center_black_line")(lbot) :
			functions.get("move_straight")(lbot)
		elif functions.get("right_black_line")(lbot) :
			functions.get("move_right")(lbot)
		elif functions.get("left_black_line")(lbot) :
			functions.get("move_left")(lbot)
		else:
			functions.get("slow_down")(lbot)
def block5():
	if activationList['start_following_red'] :
		activationList['follow_red']=True
		if not functions.get("line_crossing")(lbot) :
			activationList['start_following_red']=False
			activationList['continue_following_red']=True
def block6():
	if activationList['continue_following_red'] :
		if functions.get("line_crossing")(lbot) :
			activationList['follow_red']=False
			activationList['continue_following_red']=False
			activationList['start_following_black']=True
def block7():
	if activationList['follow_red'] :
		if functions.get("center_red_line")(lbot) :
			functions.get("move_straight")(lbot)
		elif functions.get("right_red_line")(lbot) :
			functions.get("move_right")(lbot)
		elif functions.get("left_red_line")(lbot) :
			functions.get("move_left")(lbot)
		else:
			functions.get("slow_down")(lbot)

global running
running=True

def main_loop():
	while running:
		block1()
		block2()
		block3()
		block4()
		block5()
		block6()
		block7()

import threading

main_thread=threading.Thread(target=main_loop)

main_thread.start()

while True:
	try:
		exit_prompt= input()
	except NameError:
		exit_prompt= 'q'
	if bool(exit_prompt):
		running=False
		while main_thread.is_alive():
			pass
		functions.get("stop_bot")(lbot)
		exit()
