"""
This is automatically generated python script
Author: aniq55 (C) 2017, for RoboComp Learnbot
Generated on: Sat Aug 12 07:37:49 2017
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
activationList['avoiding_right_obstacle']=False
activationList['init']=True
activationList['avoiding_left_obstacle']=False
activationList['start_avoiding']=False
activationList['always']=True

def block1():
	if functions.get("obstacle_free")(lbot) :
		functions.get("move_straight")(lbot,0,100)
		activationList['start_avoiding']=False
def block2():
	if not functions.get("obstacle_free")(lbot) and not activationList['start_avoiding'] :
		if functions.get("right_obstacle")(lbot) :
			activationList['avoiding_right_obstacle']=True
		else:
			activationList['avoiding_left_obstacle']=True
		activationList['start_avoiding']=True
def block3():
	if activationList['avoiding_right_obstacle'] :
		if not functions.get("obstacle_free")(lbot) :
			functions.get("turn_left")(lbot,0,-0.4)
		else:
			activationList['avoiding_right_obstacle']=False
def block4():
	if activationList['avoiding_left_obstacle'] :
		if not functions.get("obstacle_free")(lbot) :
			functions.get("turn_right")(lbot,0,0.4)
		else:
			activationList['avoiding_left_obstacle']=False

global running
running=True

def main_loop():
	while running:
		block1()
		block2()
		block3()
		block4()

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
