"""
This is automatically generated python script
Author: aniq55 (C) 2017, for RoboComp Learnbot
Generated on: Wed Aug  2 14:06:47 2017
"""

import sys
import cv2
import LearnBotClient
from functions import *
import time
global lbot
lbot = LearnBotClient.Client(sys.argv)
lbot.adv, lbot.rot= 0,0
# Print statement
print("The script is running")
# Variable declaration
alpha = 1 
beta=2 
# Conditional statements
if if alpha>beta :
	print("Alpha wins")
elif else if alpha == beta :
	print("Draw")
elif else if beta>alpha :
	print("Beta wins")
else:
	print("Else is working")
# Mathematical operations
gamma = alpha * beta - (alpha + beta) 
# Simple loop
for var_08109049 in range(10):
	functions.get("move_left")(lbot,2)
y1=functions.get("get_image")(lbot)
y2=functions.get("get_distance")(lbot)
y3=functions.get("get_move")(lbot)
# Alt. for loop
for i in range(1,5):
	print(5*i)
# While loop
a=5 
while a>0:
	print(a)
	a=a - 1 
# Temporal Loop
var_08109157= time.time()
while int(time.time() - var_08109157) <1:
	print(5)
functions.get("stop_bot")(lbot)
# Taking user input and deciding datatype
x = input ()
print(x)
# When block
if functions.get("front_obstacle")(lbot) and functions.get("left_obstacle")(lbot)  == True:
	print('front obstacle')
	print('left obstacle')
#no indentation error
print('invalid command')

