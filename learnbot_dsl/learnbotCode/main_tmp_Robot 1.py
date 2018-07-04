
#EXECUTION: python code_example.py config
from learnbot_dsl.functions import *
import learnbot_dsl.LearnBotClient as LearnBotClient
import sys
import time
global lbot
global Robot_id
Robot_id = "Robot 1"
try:
    lbot = LearnBotClient.Client(sys.argv, "Robot 1")
except Exception as e:
    print "hay un Error"
    print e
    
time_global_start = time.time()
def elapsedTime(umbral):
	global time_global_start
	time_global = time.time()-time_global_start
	print time_global
	return time_global > umbral


while True :
	functions.get("set_move")(lbot, 10, 0)
