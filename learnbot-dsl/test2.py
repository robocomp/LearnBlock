"""
This is automatically generated python script
Author: aniq55 (C) 2017, for RoboComp Learnbot
Generated on: Fri Jul 21 13:30:44 2017
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
if alpha>beta:
	print("Alpha wins")
elif alpha == beta:
	print("Draw")
elif beta>alpha:
	print("Beta wins")
else:
	print("Else is working")
# Mathematical operations
gamma = alpha*beta - (alpha+beta)
# Simple loop
for var_44564230 in range(10):
	functions.get("move_left")(lbot,[2])
y1=functions.get("get_image")(lbot)
y2=functions.get("get_distance")(lbot)
y3=functions.get("get_move")(lbot)
# Alt. for loop
for i in range(1,5):
	print(5*i)
	functions.get("set_move")(lbot,[5*i,0])
# While loop
a=5
while a>0:
	print(a)
	a=a-1
# Temporal Loop
var_44564291= time.time()
while int(time.time() - var_44564291) <1:
	print(5)
functions.get("stop_bot")(lbot,[])
# Taking user input and deciding datatype
x = input()
print(x)

