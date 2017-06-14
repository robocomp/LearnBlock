#
# Copyright (C) 2015 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, os, Ice

from PySide import *
from genericworker import *

import cv2
import traceback
import numpy as np
import urllib
import copy
import json
import ast
import math
#import datetime as time
from PyQt4.QtGui import *#QImage, qRgb		


ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except:
	pass
if len(ROBOCOMP)<1:
	print 'ROBOCOMP environment variable not set! Exiting.'
	sys.exit()


preStr = "-I"+ROBOCOMP+"/interfaces/ --all "+ROBOCOMP+"/interfaces/"
Ice.loadSlice(preStr+"CameraSimple.ice")
from RoboCompCameraSimple import *
Ice.loadSlice(preStr+"DifferentialRobot.ice")
from RoboCompDifferentialRobot import *
Ice.loadSlice(preStr+"Ultrasound.ice")
from RoboCompUltrasound import *


class myGraphicsSceneJoyStick(QtGui.QGraphicsScene):
  def __init__(self, parent):
    super(myGraphicsSceneJoyStick,self).__init__()    
    self.move = False
    self.press = False
    self.vaca = None
    self.vacaW = None
    self.vacaH = None
    self.parent = parent
    self.timerJoystick = QtCore.QTime.currentTime()
    
    self.setSceneRect(-100,-100,200,200)
    # Regla de 3. Para extrapolar el valor de la escena que va de 0 a 100 a los de 0 a 1024 del pwm
    # El negativo es porque en el scene el punto el 0,1 es en el centro hacia abajo.
    self.vAdvanceRobot = -800/100
    # No le pongo el negativo porque izquierda y derecha es correcto.
    self.vRotationRobot = .1#10/100
    
    posX = 0
    posY = 0
    self.vaca = self.addEllipse(posX-5,posY-5,10,10)      
    self.crosslineW = QtCore.QLineF(-self.width()/2,posY,self.width()/2,posY)
    self.crosslineH = QtCore.QLineF(posX,-self.height()/2,posX,self.height()/2)
    self.vacaW = self.addLine(self.crosslineW)
    self.vacaH = self.addLine(self.crosslineH)
    self.update()
    self.parent.setRobotSpeed(0,0)
 
 
  def mousePressAndMoveEvent(self,event):
    if self.press and self.move:
      self.removeItem(self.vaca)
      self.removeItem(self.vacaW)
      self.removeItem(self.vacaH)
      posX = event.scenePos().x()
      posY = event.scenePos().y()
      self.vaca = self.addEllipse(posX-5,posY-5,10,10)      
      self.crosslineW = QtCore.QLineF(-self.width()/2,posY,self.width()/2,posY)
      self.crosslineH = QtCore.QLineF(posX,-self.height()/2,posX,self.height()/2)
      self.vacaW = self.addLine(self.crosslineW)
      self.vacaH = self.addLine(self.crosslineH)
      self.update()
      if self.timerJoystick.elapsed() > 500:
        print "Avance: ", posY*self.vAdvanceRobot, " <--> Rotacion: ", posX*self.vRotationRobot
	self.parent.setRobotSpeed(posY*self.vAdvanceRobot,posX*self.vRotationRobot)
	self.timerJoystick.restart()
  
  def mousePressEvent(self,event):
    self.press = True
    self.mousePressAndMoveEvent(event)
    
  def mouseMoveEvent(self,event):
    self.move = True
    self.mousePressAndMoveEvent(event)
    
  def mouseReleaseEvent(self,event):
    self.press = False
    self.move = False
   
    self.removeItem(self.vaca)
    self.removeItem(self.vacaW)
    self.removeItem(self.vacaH)
    posX = 0
    posY = 0
    self.vaca = self.addEllipse(posX-5,posY-5,10,10)      
    self.crosslineW = QtCore.QLineF(-self.width()/2,posY,self.width()/2,posY)
    self.crosslineH = QtCore.QLineF(posX,-self.height()/2,posX,self.height()/2)
    self.vacaW = self.addLine(self.crosslineW)
    self.vacaH = self.addLine(self.crosslineH)
    self.update()
    self.parent.setRobotSpeed(0,0)
    
    

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)

################################
################################
		self.sceneCamera = QtGui.QGraphicsScene()

		self.qimage = QtGui.QImage(320,240,QtGui.QImage.Format_RGB888)		   
		self.ui.graphicsViewCamera.setScene(self.sceneCamera)
		
#		self.cap = cv2.VideoCapture('http://odroid.local:8080/?action=stream')
		self.stream = urllib.urlopen('http://odroid.local:8080/?action=stream')
		self.bytes=''		

################################
################################
		self.sceneUltrasound = QtGui.QGraphicsScene()
				
		self.sceneUltrasound.setSceneRect(-100,-100,200,200)
#		self.ui.graphicsViewUltrasound.scale(-1,1)
		self.ui.graphicsViewUltrasound.setScene(self.sceneUltrasound)
		
		self.sceneUltrasound.addEllipse(-5,-5,10,10)
		
		self.oveja = None
		self.gatoN = None
		self.gatoS = None
		self.gatoE = None
		self.gatoW = None	
################################
		
		self.sceneJoyStick = myGraphicsSceneJoyStick(self)
		self.vaca = self.ui.graphicsViewJoyStick.setScene(self.sceneJoyStick)
		self.sceneJoyStick.update()

		self.timer.timeout.connect(self.computeCamera)
		self.PeriodCamera = 2
		self.timer.start(self.PeriodCamera)

		self.timerU = QtCore.QTimer(self)
		self.timerU.timeout.connect(self.computeUltrasound)
		self.PeriodUltrasound = 300
		self.timerU.start(self.PeriodUltrasound)



	def setParams(self, params):
		#// 	try
		#// 	{
		#// 		RoboCompCommonBehavior::Parameter par = params.at("InnerModelPath");
		#// 		innermodel_path=par.value;
		#// 		innermodel = new InnerModel(innermodel_path);
		#// 	}
		#// 	catch(std::exception e) { qFatal("Error reading config params"); }
		return True

	@QtCore.Slot()
	def computeCamera(self):
#		print 'SpecificWorker.compute...'
		self.getImageStream()
		return True

	@QtCore.Slot()
	def computeUltrasound(self):
#		print 'SpecificWorker.compute...'	
		self.getUltrasound()
		return True

	def getImageStream(self):
	    self.bytes += self.stream.read(1024)	    
	    a = self.bytes.find('\xff\xd8')
	    b = self.bytes.find('\xff\xd9')
	    if a!=-1 and b!=-1:
	      jpg = self.bytes[a:b+2]
	      self.bytes = self.bytes[b+2:]
	      #self.image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
	      self.image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
    #	    cv2.imshow('i',self.image)
	      try:
		self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
		self.qimage = QtGui.QImage(self.image.data,320,240,0,QtGui.QImage.Format_RGB888)	      
		self.sceneCamera.removeItem(self.oveja)     
		self.oveja = self.sceneCamera.addPixmap(QtGui.QPixmap.fromImage(self.qimage))	      
		self.sceneCamera.update()
	      except:
		print "sheep"
		return None
	    return True

	def getUltrasound(self):
#	  print 'UltrasoundReader: SpecificWorker.compute...'
	  ultrasound = ast.literal_eval(self.ultrasound_proxy.getAllSensorData())
	  marginImage = 5
	  
	  polygonN = QtGui.QPolygon()
	  polygonS = QtGui.QPolygon()
	  polygonE = QtGui.QPolygon()
	  polygonW = QtGui.QPolygon()
	  
	  if self.gatoN != None:
	    self.sceneUltrasound.removeItem(self.gatoN)
	    self.sceneUltrasound.removeItem(self.gatoS)
	    self.sceneUltrasound.removeItem(self.gatoE)	    
	    self.sceneUltrasound.removeItem(self.gatoW)
	  	      
#	  Degrees to Radians
	  radians15 = 180 * 15 / math.pi
	  radians75 = 180 * 75 / math.pi
	  radians90 = 180 * 90 / math.pi
  
	  for nombre, sensor in ultrasound.items():
	    if (nombre == "sensor0"):
	      # Sin Theorema
	      h = (math.sin(radians90) * sensor["dist"]) / math.sin(radians75)
	      a = (math.sin(radians15) * sensor["dist"]) / math.sin(radians75)	      	      
	      # p0 el 0,0 desplazado sobre la imagen de la mariquita
	      polygonN.push_back(QtCore.QPoint(0,marginImage))     
	      polygonN.push_back(QtCore.QPoint(0+a,h+marginImage))
	      polygonN.push_back(QtCore.QPoint(0-a,h+marginImage))
#	      polygonN.push_back(QtCore.QPoint(0,sensor["dist"]+marginImage))
	      polygonN.push_back(QtCore.QPoint(0,marginImage))	      
	    
	    elif (nombre == "sensor1"):
#	      polygonS.push_back(QtCore.QPoint(0,-marginImage))
#	      polygonS.push_back(QtCore.QPoint(marginImage,-(sensor["dist"]+marginImage)))
	      # Sin Theorema
	      h = (math.sin(radians90) * sensor["dist"]) / math.sin(radians75)
	      a = (math.sin(radians15) * sensor["dist"]) / math.sin(radians75)
	      polygonS.push_back(QtCore.QPoint(0,-marginImage))      
	      polygonS.push_back(QtCore.QPoint(0+a,-(h+marginImage)))
	      polygonS.push_back(QtCore.QPoint(0-a,-(h+marginImage)))
	      polygonS.push_back(QtCore.QPoint(0,-marginImage))	
	      
	    elif (nombre == "sensor2"):
#	      polygonE.push_back(QtCore.QPoint(marginImage,0))
#	      polygonE.push_back(QtCore.QPoint(sensor["dist"]+marginImage,0))	
	      # Sin Theorema
	      h = (math.sin(radians90) * sensor["dist"]) / math.sin(radians75)
	      a = (math.sin(radians15) * sensor["dist"]) / math.sin(radians75)	      
	      polygonE.push_back(QtCore.QPoint(marginImage,0))
	      polygonE.push_back(QtCore.QPoint(h+marginImage,0+a))
	      polygonE.push_back(QtCore.QPoint(h+marginImage,0-a))
	      polygonE.push_back(QtCore.QPoint(marginImage,0))
	      
	    elif (nombre == "sensor3"):
#	      polygonW.push_back(QtCore.QPoint(-marginImage,0))
#	      polygonW.push_back(QtCore.QPoint(-(sensor["dist"]+marginImage),0))
	      h = (math.sin(radians90) * sensor["dist"]) / math.sin(radians75)
	      a = (math.sin(radians15) * sensor["dist"]) / math.sin(radians75)	      
	      polygonW.push_back(QtCore.QPoint(-marginImage,0))
	      polygonW.push_back(QtCore.QPoint(-(h+marginImage),0+a))
	      polygonW.push_back(QtCore.QPoint(-(h+marginImage),0-a))
	      polygonW.push_back(QtCore.QPoint(-marginImage,0))

	    else:
	      print "sheep"
	      
	  self.gatoN = self.sceneUltrasound.addPolygon(polygonN)
	  self.gatoS = self.sceneUltrasound.addPolygon(polygonS)
	  self.gatoE = self.sceneUltrasound.addPolygon(polygonE)
	  self.gatoW = self.sceneUltrasound.addPolygon(polygonW)
	  self.sceneUltrasound.update()

	  return True	
	
	
	def setRobotSpeed(self,vAdvance,vRotation):	  
	  self.differentialrobot_proxy.setSpeedBase(vAdvance,vRotation)	  	  
	  return True
	  
