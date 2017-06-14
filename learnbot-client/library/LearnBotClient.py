#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, traceback, Ice, os, math, time, json, ast
import json
import cv2
import urllib
from collections import namedtuple
import numpy as np

Ice.loadSlice("slices/Ultrasound.ice")
Ice.loadSlice("slices/DifferentialRobot.ice")

import RoboCompUltrasound
import RoboCompDifferentialRobot


import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

ic = None


		
class Client(Ice.Application):	
	def __init__(self, clase):
		self.clase = clase		
		
	def run(self, argv):
#	  	ic = Ice.initialize(sys.argv)
		print ("RUN!")
	  	global ic
	  	ic = self.communicator()
		status = 0
		try:
			# Remote object connection for DifferentialRobot
			try:
				proxyString = ic.getProperties().getProperty('DifferentialRobotProxy')
				try:
					basePrx = ic.stringToProxy(proxyString)
					self.differentialrobot_proxy = RoboCompDifferentialRobot.DifferentialRobotPrx.checkedCast(basePrx)
				except Ice.Exception:
					print ('Cannot connect to the remote object (DifferentialRobot)', proxyString)
					sys.exit(1)
			except Ice.Exception, e:
				print (e)
				print ('Cannot get DifferentialRobotProxy property.')
				sys.exit(1)
			# Remote object connection for Ultrasound
			try:
				proxyString = ic.getProperties().getProperty('UltrasoundProxy')
				try:
					basePrx = ic.stringToProxy(proxyString)
					self.ultrasound_proxy = RoboCompUltrasound.UltrasoundPrx.checkedCast(basePrx)
				except Ice.Exception:
					print ('Cannot connect to the remote object (Ultrasound)', proxyString)
					sys.exit(1)
			except Ice.Exception, e:
				print (e)
				print ('Cannot get UltrasoundProxy property.')
				sys.exit(1)
		except:
				traceback.print_exc()
				sys.exit(1)	 
		self.code()


	def getSonars(self):
		return self.ultrasound_proxy.getAllSensorData()
		#print self.ultrasound_proxy.getAllSensorData()
	 	     
	 	     
	def setRobotSpeed(self, vAdvance, vRotation):
		#print "Velocidad de avance: "+str(vAdvance)+". Velocidad de giro: "+str(vRotation)+"."
		self.differentialrobot_proxy.setSpeedBase(vAdvance,vRotation)	 
				
	def getImage(self):
		stream = urllib.urlopen('http://odroid.local:8080/?action=stream')
		bytes=''
		Frame = False
		while Frame is False:
		  bytes += stream.read(1024)	    
		  a = bytes.find('\xff\xd8')
		  b = bytes.find('\xff\xd9')
		  if a!=-1 and b!=-1:
		    jpg = bytes[a:b+2]
		    bytes = bytes[b+2:]
		    #image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
		    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

		    Frame = True
		   # print 'Got Picture!'
	#	cv2.imshow('FrameCapture',image)
		return image
	      
	      
	def facesDetect(self, frame, faceCascadePath, draw):
		faceCascade = cv2.CascadeClassifier(faceCascadePath)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30),
		flags=cv2.cv.CV_HAAR_SCALE_IMAGE
	        )
		if draw is True:
			# Draw a rectangle around the faces
			for (x, y, w, h) in faces:
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		else:
			print (faces)

############################################################################################
	def avanza(self, metros):
		tiempo = float(metros/0.05)
		print ("||  Para ",metros,"metros , avanza durante ",tiempo," segundos")
		#self.setRobotSpeed(1024, 0.47)
		self.setRobotSpeed(1024, 0)
		time.sleep(tiempo)
		
	def gira(self, grados):
		tiempo = grados/float(90)#s+0.27		
		print ("||  Para ",grados," grados, gira durante ",tiempo," segundos")
		self.setRobotSpeed(0, 13)
		time.sleep(tiempo)		
		
	def para(self):
		print ("PARANDO!!")
		self.setRobotSpeed(0,0)
	
	def corre(self):
		print ("CORRIENDO!!!")
		self.setRobotSpeed(1000,0)
############################################################################################
	def reconocerCara(self):
		while True:
			image       = self.getImage()
			faceCascade = "haarcascades/haarcascade_frontalface_default.xml" 
			self.facesDetect(image, faceCascade, True)
			cv2.imshow('img',image)
			if cv2.waitKey(1)&0xff==ord('q'):
				break
############################################################################################
	def obtenerDistancia(self):	    
	    jsonSonars = ast.literal_eval(self.getSonars())
	    return jsonSonars["sensor1"]["dist"]
	

