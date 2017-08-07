"""
This is automatically generated python script
Author: aniq55 (C) 2017, for RoboComp Learnbot
Generated on: Mon Aug  7 20:44:33 2017
"""

import sys
import cv2
import threading
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
activationList['var2']=True
activationList['continue_following_black']=False
activationList['init']=False
activationList['start_following_red']=False
activationList['start_following_black']=False
activationList['continue_following_red']=False
activationList['always']=True
activationList['init']=True

def block1():
	if activationList['init'] :
		activationList['start_following_black']=True
		activationList['init']=False
def block2():
	if activationList['start_following_black'] :
		activationList['follow_black']=True
		if not functions.get("line_crossing")(lbot) :
			activationList['start_following_black']=False
def block3():
	if activationList['continue_following_black'] or functions.get("left_black_line")(lbot) :
		if functions.get("line_crossing")(lbot) :
			activationList['follow_black']=False
			activationList['continue_following_black']=False
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
def block6():
	if activationList['continue_following_red'] :
		if functions.get("line_crossing")(lbot) :
			activationList['follow_red']=False
			activationList['continue_following_red']=False
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

#Running the when blocks concurrently
def main_loop():
	jobs=[]
	for i in range(7):
		process=threading.Thread(target=block1)
		process.start()
		jobs.append(process)
		process=threading.Thread(target=block2)
		process.start()
		jobs.append(process)
		process=threading.Thread(target=block3)
		process.start()
		jobs.append(process)
		process=threading.Thread(target=block4)
		process.start()
		jobs.append(process)
		process=threading.Thread(target=block5)
		process.start()
		jobs.append(process)
		process=threading.Thread(target=block6)
		process.start()
		jobs.append(process)
		process=threading.Thread(target=block7)
		process.start()
		jobs.append(process)
	for j in jobs:
		j.join()


while True:
	try:
		main_loop()
	except KeyboardInterrupt:
		break

