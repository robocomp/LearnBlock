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
Ice.loadSlice(preStr+"Laser.ice")
Ice.loadSlice(preStr+"DifferentialRobot.ice")
Ice.loadSlice(preStr+"JointMotor.ice")
Ice.loadSlice(preStr+"GenericBase.ice")

import RoboCompRGBD
import RoboCompLaser
import RoboCompDifferentialRobot
import RoboCompJointMotor
import RoboCompGenericBase


import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

ic = None


		
class Client(Ice.Application, threading.Thread):	
	def __init__(self, argv):
		threading.Thread.__init__(self)

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
			# Remote object connection for Laser1
			try:
				proxyString = ic.getProperties().getProperty('Laser1Proxy')
				try:
					basePrx = ic.stringToProxy(proxyString)
					self.laser1_proxy = RoboCompLaser.LaserPrx.checkedCast(basePrx)
				except Ice.Exception:
					print 'Cannot connect to the remote object (Laser)', proxyString
					sys.exit(1)
			except Ice.Exception, e:
				print e
				print 'Cannot get Laser1Proxy property.'
				sys.exit(1)
			# Remote object connection for Laser2
			try:
				proxyString = ic.getProperties().getProperty('Laser2Proxy')
				try:
					basePrx = ic.stringToProxy(proxyString)
					self.laser2_proxy = RoboCompLaser.LaserPrx.checkedCast(basePrx)
				except Ice.Exception:
					print 'Cannot connect to the remote object (Laser)', proxyString
					sys.exit(1)
			except Ice.Exception, e:
				print e
				print 'Cannot get Laser2Proxy property.'
				sys.exit(1)
			# Remote object connection for Laser3
			try:
				proxyString = ic.getProperties().getProperty('Laser3Proxy')
				try:
					basePrx = ic.stringToProxy(proxyString)
					self.laser3_proxy = RoboCompLaser.LaserPrx.checkedCast(basePrx)
				except Ice.Exception:
					print 'Cannot connect to the remote object (Laser)', proxyString
					sys.exit(1)
			except Ice.Exception, e:
				print e
				print 'Cannot get Laser3Proxy property.'
				sys.exit(1)
			# Remote object connection for Laser4
			try:
				proxyString = ic.getProperties().getProperty('Laser4Proxy')
				try:
					basePrx = ic.stringToProxy(proxyString)
					self.laser4_proxy = RoboCompLaser.LaserPrx.checkedCast(basePrx)
				except Ice.Exception:
					print 'Cannot connect to the remote object (Laser)', proxyString
					sys.exit(1)
			except Ice.Exception, e:
				print e
				print 'Cannot get Laser4Proxy property.'
				sys.exit(1)
			# Remote object connection for RGBD
			try:
				proxyString = ic.getProperties().getProperty('RGBDProxy')
				try:
					basePrx = ic.stringToProxy(proxyString)
					self.rgbd_proxy = RoboCompRGBD.RGBDPrx.checkedCast(basePrx)
				except Ice.Exception:
					print 'Cannot connect to the remote object (RGBD)', proxyString
					sys.exit(1)
			except Ice.Exception, e:
				print e
				print 'Cannot get RGBDProxy property.'
				sys.exit(1)




		except:
				traceback.print_exc()
				sys.exit(1)	 

		self.active = True
		self.start()

		
	def run(self):
		while self.active:
			try:
				self.color, self.depth, self.headState, self.baseState = self.rgbd_proxy.getData()
				if (len(self.color) == 0) or (len(self.depth) == 0):
	                                print 'Error retrieving images!'
	                except Ice.Exception:
	                        traceback.print_exc()		
	
			self.image = np.fromstring(self.color, dtype=np.uint8).reshape((240, 320, 3))

			self.readSonars()

			time.sleep(0.01)

	def readSonars(self):

		l1data = self.laser1_proxy.getLaserData()
		minD1 = l1data[0].dist
		for data in l1data:
			if minD1 > data.dist:
				minD1 = data.dist
	
		self.usList["front"] = minD1

		l2data = self.laser2_proxy.getLaserData()
		minD2 = l2data[0].dist
		for data in l2data:
			if minD2 > data.dist:
				minD2 = data.dist

		self.usList["right"] = minD2


		l3data = self.laser3_proxy.getLaserData()
		minD3 = l3data[0].dist
		for data in l3data:
			if minD3 > data.dist:
				minD3 = data.dist

		self.usList["left"] = minD2


		l4data = self.laser4_proxy.getLaserData()
		minD4 = l4data[0].dist
		for data in l4data:
			if minD4 > data.dist:
				minD4 = data.dist

		self.usList["back"] = minD2



	def getSonars(self):
		return self.usList

	def getImage(self):
		return self.image

	def getPose(self):
		x, y, alpha = self.differentialrobot_proxy.getBasePose()	 
		return x, y, alpha
	 	     
	def setRobotSpeed(self, vAdvance=0, vRotation=0):
		if vAdvance!=0 or vRotation!=0:
			self.adv = vAdvance
			self.rot = vRotation
		self.differentialrobot_proxy.setSpeedBase(self.adv,self.rot)	 
				

	def __del__(self):
        	self.active = False


	      
	

