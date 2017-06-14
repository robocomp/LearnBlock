import sys
import cv2
import LearnBotClient
from functions import *
import time

global lbot
lbot = LearnBotClient.Client(sys.argv)


#####################
#	 CODE BEGINS	#
#####################

# To keep track of the speed of Learnbot
lbot.adv, lbot.rot= 0,0
	

# MOVEMENTS

functions.get("move_right")(lbot,3)
functions.get("move_left")(lbot)
time.sleep(2)
functions.get("move_right")(lbot)
time.sleep(3)
functions.get("move_left")(lbot,4)
functions.get("move_straight")(lbot)
time.sleep(3)
functions.get("turn_back")(lbot)
functions.get("move_straight")(lbot)
time.sleep(3)
functions.get("set_move")(lbot,[100,0.5])
time.sleep(10)
functions.get("get_move")(lbot)
functions.get("turn")(lbot, 45)
functions.get("stop_bot")(lbot)

# GETTING DISTANCE

print functions.get("get_distance")(lbot)


# GETTING IMAGE FROM CAMERA

current_image = functions.get("get_image")(lbot)
# cv2.imwrite('temp_image.png', current_image)	#saving the image