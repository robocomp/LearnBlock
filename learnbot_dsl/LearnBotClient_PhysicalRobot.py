#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, traceback, Ice, os, math, time, json, ast, copy, threading
import json
import cv2
import urllib
from collections import namedtuple
import numpy as np

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
	print '$ROBOCOMP environment variable not set, using the default value /opt/robocomp'
	ROBOCOMP = '/opt/robocomp'

preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"

Ice.loadSlice(preStr+"RGBD.ice")
Ice.loadSlice(preStr+"Ultrasound.ice")
Ice.loadSlice(preStr+"DifferentialRobot.ice")
Ice.loadSlice(preStr+"JointMotor.ice")
Ice.loadSlice(preStr+"GenericBase.ice")

import RoboCompRGBD
import RoboCompUltrasound
import RoboCompDifferentialRobot
import RoboCompJointMotor
import RoboCompGenericBase


import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

ic = None


		
class Client(Ice.Application, threading.Thread):	
	def __init__(self, argv):
		threading.Thread.__init__(self)

		self.mutex = threading.Lock()

		self.adv = 0
		self.rot = 0
		self.max_rot= 0.4
		self.image = np.zeros((240,320,3), np.uint8)
		self.usList = {'front':1000, 'right':1000, 'left':1000, 'back':1000}

	  	global ic

		params = copy.deepcopy(sys.argv)
		if len(params) > 1:
			if not params[1].startswith('--Ice.Config='):
				params[1] = '--Ice.Config=' + params[1]
		elif len(params) == 1:
			params.append('--Ice.Config=config')
		ic = Ice.initialize(params)


		status = 0
		try:
			# Remote object connection for DifferentialRobot
			try:
				proxyString = ic.getProperties().getProperty('DifferentialRobotProxy')
				try:
					basePrx = ic.stringToProxy(proxyString)
					self.differentialrobot_proxy = RoboCompDifferentialRobot.DifferentialRobotPrx.checkedCast(basePrx)
				except Ice.Exception:
					print 'Cannot connect to the remote object (DifferentialRobot)', proxyString
					sys.exit(1)
			except Ice.Exception, e:
				print e
				print 'Cannot get DifferentialRobotProxy property.'
				sys.exit(1)
			# Remote object connection for Ultrasound
			try:
				proxyString = ic.getProperties().getProperty('UltrasoundProxy')
				try:
					basePrx = ic.stringToProxy(proxyString)
					self.ultrasound_proxy = RoboCompUltrasound.UltrasoundPrx.checkedCast(basePrx)
				except Ice.Exception:
					print 'Cannot connect to the remote object (Ultrasound)', proxyString
					sys.exit(1)
			except Ice.Exception, e:
				print e
				print 'Cannot get UltrasoundProxy property.'
				sys.exit(1)

			self.stream = urllib.urlopen('http://odroid.local:8080/?action=stream')
			self.bytes=''	



		except:
				traceback.print_exc()
				sys.exit(1)	 

		self.active = True
		self.start()

		
	def run(self):
		while self.active:

			self.getImageStream()
			self.readSonars()

			time.sleep(0.002)


	def getImageStream(self):
		self.bytes += self.stream.read(5120)	    
		a = self.bytes.find('\xff\xd8')
		b = self.bytes.find('\xff\xd9')
		if a!=-1 and b!=-1:
			jpg = self.bytes[a:b+2]
			self.bytes = self.bytes[b+2:]
			image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
			try:
				tempimage = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
				image = cv2.flip(tempimage, 0)
			except:
				print "Error retrieving images!"
				return None
			self.mutex.acquire()
			self.image = image
			self.mutex.release()
		return True


	def readSonars(self):
		ultrasound = ast.literal_eval(self.ultrasound_proxy.getAllSensorData())

		for nombre, sensor in ultrasound.items():
			if (nombre == "sensor0"):
				self.usList["front"] = sensor["dist"]
			elif (nombre == "sensor1"):
				self.usList["back"] = sensor["dist"]
			elif (nombre == "sensor2"):
				self.usList["right"] = sensor["dist"]
			elif (nombre == "sensor3"):
				self.usList["left"] = sensor["dist"]


	def getSonars(self):
		return self.usList

	def getImage(self):
		self.mutex.acquire()
		simage = self.image
		self.mutex.release()
		
		return simage

	def getPose(self):
		x, y, alpha = self.differentialrobot_proxy.getBasePose()	 
		return x, y, alpha
	 	     
	def setRobotSpeed(self, vAdvance=0, vRotation=0):
		print vAdvance, vRotation
		if vAdvance!=0 or vRotation!=0:
			self.adv = -vAdvance*10
			self.rot = vRotation*14
		self.differentialrobot_proxy.setSpeedBase(self.adv,self.rot)	 
				

	def __del__(self):
        	self.active = False


	      
	

