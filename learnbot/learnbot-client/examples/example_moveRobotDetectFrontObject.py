import sys, time
import LearnBotClient
import ast

# Ctrl+c handling
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class MiClase(LearnBotClient.Client):
  def __init__(self):
    pass

  def code(self):
    i=0
    detect = False
    
    while True:      
      if detect is False:
	i+=100
	self.setRobotSpeed(i,0)	
	      
	sonarsValue = ast.literal_eval(self.getSonars())
	for name, sensor in sonarsValue.items():
	  if sensor["dist"] < 20:
	    detect = True
	    i = 0
	    self.setRobotSpeed(0,0)
	
      time.sleep(0.25) 
miclase = MiClase()
miclase.main(sys.argv)