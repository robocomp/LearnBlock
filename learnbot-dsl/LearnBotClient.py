#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, traceback, Ice, os, math, time, json, ast, copy
import json
# import cv
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


		
class Client(Ice.Application):	
	def __init__(self, argv):
	  	global ic

		self.adv = 0
		self.rot = 0

		params = copy.deepcopy(sys.argv)
		if len(params) > 1:
			if not params[1].startswith('--Ice.Config='):
				params[1] = '--Ice.Config=' + params[1]
		elif len(params) == 1:
			params.append('--Ice.Config=config')
		ic = Ice.initialize(params)


#	  	ic = self.communicator()

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

		
	def run(self):
		pass

	def getSonars(self):
		usList = {}

		l1data = self.laser1_proxy.getLaserData()
		minD1 = l1data[0].dist
		for data in l1data:
			if minD1 > data.dist:
				minD1 = data.dist
	
		usList["front"] = minD1

		l2data = self.laser2_proxy.getLaserData()
		minD2 = l2data[0].dist
		for data in l2data:
			if minD2 > data.dist:
				minD2 = data.dist

		usList["right"] = minD2


		l3data = self.laser3_proxy.getLaserData()
		minD3 = l3data[0].dist
		for data in l3data:
			if minD3 > data.dist:
				minD3 = data.dist

		usList["left"] = minD2


		l4data = self.laser4_proxy.getLaserData()
		minD4 = l4data[0].dist
		for data in l4data:
			if minD4 > data.dist:
				minD4 = data.dist

		usList["back"] = minD2

		return usList	 	     
	 	     
	def setRobotSpeed(self, vAdvance, vRotation):
		self.differentialrobot_proxy.setSpeedBase(vAdvance,vRotation)	 
				
	def getImage(self):
		try:
			self.color, self.depth, self.headState, self.baseState = self.rgbd_proxy.getData()
			if (len(self.color) == 0) or (len(self.depth) == 0):
                                print 'Error retrieving images!'
                except Ice.Exception:
                        traceback.print_exc()		

		self.image = np.fromstring(self.color, dtype=np.uint8).reshape((240, 320, 3))
		
		return self.image

	def code(self):
		while True:		
			pass

	      
	

