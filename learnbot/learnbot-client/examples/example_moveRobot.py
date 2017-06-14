import sys, time
import LearnBotClient

# Ctrl+c handling
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class MiClase(LearnBotClient.Client):
  def __init__(self):
    pass

  def code(self):
    i=0
    incrementarV = True
    adelante = True
    completadoAdelante = False
    completadoAtras = False
    
    while True:
      while completadoAdelante is False:
	if incrementarV is True:
	  i+=10
	else:
	  i-=10
	  
	self.setRobotSpeed(i,0)	
	if i >= 1024:
	  incrementarV = False
	if i <= -1024:
	  incrementarV = True
	  completadoAdelante = True
	time.sleep(0.25)
      incrementarV = True
      while completadoAtras is False:
	if incrementarV is True:
	  i+=10
	else:
	  i-=10
      
	self.setRobotSpeed(i,0)	
	if i >= 1024:
	  incrementarV = False
	if i <= -1024:
	  incrementarV = True
	  completadoAtras = True
	time.sleep(0.25)
      
      
miclase = MiClase()
miclase.main(sys.argv)