# -*- coding: utf-8 -*-
import numpy as np
import cv2

import ast
import sys, time
import LearnBotClient

# Ctrl+c handling
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class MiClase(LearnBotClient.Client):
  def __init__(self):
    frame = self.getImage()
    self.height = frame.shape[0]
    self.width = frame.shape[1]

  def code(self):  
    encontrado = False
    while(True):
      print encontrado
      # Capture frame-by-frame
      frame = self.getImage()
      # Concertir a gris
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      # Gaussian filtering
      grayG = cv2.GaussianBlur(gray,(5,5),0)
      # Otsu's thresholding
      ret2, otsu = cv2.threshold(grayG, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
      #Compute virtual sensors
      col = self.width/3
      sv = []

      cv2.rectangle(frame,(self.width/3-10,self.height-40),(self.width/3+10,self.height),(255,0,0))      
      cv2.rectangle(frame,(self.width/2-10,self.height-40),(self.width/2+10,self.height),(0,255,0))    
      cv2.rectangle(frame,(2*self.width/3-10,self.height-40),(2*self.width/3+10,self.height),(255,0,0))
      sv.append((otsu[self.height-40:self.height,1*col-10:1*col+10] == 0).sum())	
      sv.append((otsu[self.height-40:self.height,1*self.width/2-10:1*self.width/2+10] == 0).sum())
      sv.append((otsu[self.height-40:self.height,1*2*self.width/3-10:1*2*self.width/3+10] == 0).sum())
      
      a=sv
      # compute advance speed prop to len(linea)
      max=0
      maxIndex=1
      for i in range(len(a)):
	if a[i] > max:
	    max = a[i]
	    maxIndex = i
      
      sonarsValue = ast.literal_eval(self.getSonars())
      numWall=0
      for name, sensor in sonarsValue.items():
        # 0 atras -- 1 delante -- 2 derecha -- 3 izquierda
	if sensor["dist"]<20 and name == "sensor1" and encontrado is False:
	  self.setRobotSpeed(0,0)
	  print "pared detectada"
	  time.sleep(4)
	  print "A POR ELLA!!!"
	  encontrado = True
	elif sensor["dist"]<20 and name == "sensor1" or (sensor["dist"]<20 and name == "sensor2" or sensor["dist"]<20) and encontrado is True:
	  if numWall >= 2:
	    self.setRobotSpeed(0,0)
	    print "He llegado a casa :-)"
	    sys.exit(1)
	  else:
	    numWall+=1
	if encontrado is False:
	  if maxIndex is 0:
	    print "gira derecha"
	    self.setRobotSpeed(150,-3)
	  elif maxIndex is 2:
	    print "gira izquierda"
	    self.setRobotSpeed(150,3)    
	  elif maxIndex is 1:
	    print "recto"
	    self.setRobotSpeed(450,0)
	else:
	  print "Quiero llegar a casa"
	  self.setRobotSpeed(750,0)
  # Display the resulting frame
      cv2.imshow('edges',otsu)  
      cv2.imshow('frame',frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
	      break

# When everything done, release the capture
cv2.destroyAllWindows()

miclase = MiClase()
miclase.main(sys.argv)