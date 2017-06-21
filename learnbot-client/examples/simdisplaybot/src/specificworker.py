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
import cv
import traceback
import numpy as np
import urllib
import copy
import json
import ast
import math
#import datetime as time
from PyQt4.QtGui import *#QImage, qRgb

#To make it compatible with python 3
from __future__ import print_function
from __future__ import division

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except:
	pass
if len(ROBOCOMP)<1:
	print ('ROBOCOMP environment variable not set! Exiting.')
	sys.exit()


preStr = "-I"+ROBOCOMP+"/interfaces/ --all "+ROBOCOMP+"/interfaces/"
Ice.loadSlice(preStr+"RGBD.ice")
from RoboCompRGBD import *
Ice.loadSlice(preStr+"DifferentialRobot.ice")
from RoboCompDifferentialRobot import *
Ice.loadSlice(preStr+"Laser.ice")
from RoboCompLaser import *


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
    self.vAdvanceRobot = 10
    self.vRotationRobot = 0.05
    
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
      print ("Advance speed:", -posY*self.vAdvanceRobot, " <--> Rotation speed: ", posX*self.vRotationRobot)
      self.parent.setRobotSpeed(-posY*self.vAdvanceRobot,posX*self.vRotationRobot)
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
		
		self.bytes=''		

################################
################################
		self.sceneUltrasound = QtGui.QGraphicsScene()
				
		self.sceneUltrasound.setSceneRect(-100,-100,200,200)
#		self.ui.graphicsViewUltrasound.scale(-1,1)
		self.ui.graphicsViewUltrasound.setScene(self.sceneUltrasound)
		
		self.sceneUltrasound.addEllipse(-5,-5,10,10)
		
		self.gatoN = None
		self.gatoS = None
		self.gatoE = None
		self.gatoW = None	
################################
		
		self.sceneJoyStick = myGraphicsSceneJoyStick(self)
		self.vaca = self.ui.graphicsViewJoyStick.setScene(self.sceneJoyStick)
		self.sceneJoyStick.update()

		self.timer.timeout.connect(self.getImage)
		self.PeriodCamera = 33
		self.timer.start(self.PeriodCamera)

		self.timerU = QtCore.QTimer(self)
		self.timerU.timeout.connect(self.computeUltrasound)
		self.PeriodUltrasound = 33
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
	def getImage(self):
#		print 'SpecificWorker.compute...'
		try:
			self.color, self.depth, self.headState, self.baseState = self.rgbd_proxy.getData()
			if (len(self.color) == 0) or (len(self.depth) == 0):
                                print ('Error retrieving images!')
                except Ice.Exception:
                        traceback.print_exc()		

		self.imageArr = np.fromstring(self.color, dtype=np.uint8).reshape((240, 320, 3))
		try:
			self.qimage = QtGui.QImage(self.imageArr,320,240,0,QtGui.QImage.Format_RGB888)	      
			self.sceneCamera.addPixmap(QtGui.QPixmap.fromImage(self.qimage))	      
			self.sceneCamera.update()
		except:
			print ("problem showing image...")
			return None
	


		#self.getImageStream()
		return True

	@QtCore.Slot()
	def computeUltrasound(self):

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


		usData = self.getUltrasound()

		usData[0] = usData[0]/10

		h = (math.sin(radians90) * usData[0]) / math.sin(radians75)
		a = (math.sin(radians15) * usData[0]) / math.sin(radians75)	      	      
		polygonN.push_back(QtCore.QPoint(0,-marginImage))      
		polygonN.push_back(QtCore.QPoint(0+a,-(h+marginImage)))
		polygonN.push_back(QtCore.QPoint(0-a,-(h+marginImage)))
		polygonN.push_back(QtCore.QPoint(0,-marginImage))	


		usData[1] = usData[1]/10

		h = (math.sin(radians90) * usData[1]) / math.sin(radians75)
		a = (math.sin(radians15) * usData[1]) / math.sin(radians75)	      
		polygonE.push_back(QtCore.QPoint(-marginImage,0))
		polygonE.push_back(QtCore.QPoint(-(h+marginImage),0+a))
		polygonE.push_back(QtCore.QPoint(-(h+marginImage),0-a))
		polygonE.push_back(QtCore.QPoint(-marginImage,0))


		usData[2] = usData[2]/10

		h = (math.sin(radians90) * usData[2]) / math.sin(radians75)
		a = (math.sin(radians15) * usData[2]) / math.sin(radians75)	      
		polygonW.push_back(QtCore.QPoint(marginImage,0))
		polygonW.push_back(QtCore.QPoint(h+marginImage,0+a))
		polygonW.push_back(QtCore.QPoint(h+marginImage,0-a))
		polygonW.push_back(QtCore.QPoint(marginImage,0))


		usData[3] = usData[3]/10

		h = (math.sin(radians90) * usData[3]) / math.sin(radians75)
		a = (math.sin(radians15) * usData[3]) / math.sin(radians75)
		polygonS.push_back(QtCore.QPoint(0,marginImage))     
		polygonS.push_back(QtCore.QPoint(0+a,h+marginImage))
		polygonS.push_back(QtCore.QPoint(0-a,h+marginImage))
		polygonS.push_back(QtCore.QPoint(0,marginImage))	

		self.gatoN = self.sceneUltrasound.addPolygon(polygonN)
		self.gatoS = self.sceneUltrasound.addPolygon(polygonS)
		self.gatoE = self.sceneUltrasound.addPolygon(polygonE)
		self.gatoW = self.sceneUltrasound.addPolygon(polygonW)
		self.sceneUltrasound.update()

		return True

	def getUltrasound(self):

		usList = []

		l1data = self.laser1_proxy.getLaserData()
		minD1 = l1data[0].dist
		for data in l1data:
			if minD1 > data.dist:
				minD1 = data.dist

		usList.append(minD1)

		l2data = self.laser2_proxy.getLaserData()
		minD2 = l2data[0].dist
		for data in l2data:
			if minD2 > data.dist:
				minD2 = data.dist

		usList.append(minD2)

		l3data = self.laser3_proxy.getLaserData()
		minD3 = l3data[0].dist
		for data in l3data:
			if minD3 > data.dist:
				minD3 = data.dist

		usList.append(minD3)

		l4data = self.laser4_proxy.getLaserData()
		minD4 = l4data[0].dist
		for data in l4data:
			if minD4 > data.dist:
				minD4 = data.dist

		usList.append(minD4)

		return usList

	
	def setRobotSpeed(self,vAdvance,vRotation):	  
	  self.differentialrobot_proxy.setSpeedBase(vAdvance,vRotation)	  	  
	  return True
	  
