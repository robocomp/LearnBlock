"""
This is automatically generated python script
Author: aniq55 (C) 2017, for RoboComp Learnbot
Generated on: Sat Aug 12 18:09:18 2017
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
activationList['always']=True
activationList['init']=True

def block1():
	if functions.get("obstacle_free")(lbot) :
		functions.get("move_straight")(lbot,0,100)
def block2():
	if not functions.get("obstacle_free")(lbot) :
		functions.get("turn_right")(lbot,0,0.4)

global running
running=True

def main_loop():
	while running:
		block1()
		block2()

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
