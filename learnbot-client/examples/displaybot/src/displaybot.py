#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# \mainpage RoboComp::displaybot
#
# \section intro_sec Introduction
#
# Some information about the component...
#
# \section interface_sec Interface
#
# Descroption of the interface provided...
#
# \section install_sec Installation
#
# \subsection install1_ssec Software depencences
# Software dependences....
#
# \subsection install2_ssec Compile and install
# How to compile/install the component...
#
# \section guide_sec User guide
#
# \subsection config_ssec Configuration file
#
# <p>
# The configuration file...
# </p>
#
# \subsection execution_ssec Execution
#
# Just: "${PATH_TO_BINARY}/displaybot --Ice.Config=${PATH_TO_CONFIG_FILE}"
#
# \subsection running_ssec Once running
#
#
#
from __future__ import print_function
import sys, traceback, Ice, IceStorm, subprocess, threading, time, Queue, os

# Ctrl+c handling
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from PySide import *

from specificworker import *

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except:
	pass
if len(ROBOCOMP)<1:
	print('ROBOCOMP environment variable not set! Exiting.')
	sys.exit()


preStr = "-I"+ROBOCOMP+"/interfaces/ --all "+ROBOCOMP+"/interfaces/"
Ice.loadSlice(preStr+"CommonBehavior.ice")
import RoboCompCommonBehavior
Ice.loadSlice(preStr+"DifferentialRobot.ice")
import RoboCompDifferentialRobot
Ice.loadSlice(preStr+"Ultrasound.ice")
import RoboCompUltrasound


class CommonBehaviorI(RoboCompCommonBehavior.CommonBehavior):
	def __init__(self, _handler, _communicator):
		self.handler = _handler
		self.communicator = _communicator
	def getFreq(self, current = None):
		self.handler.getFreq()
	def setFreq(self, freq, current = None):
		self.handler.setFreq()
	def timeAwake(self, current = None):
		try:
			return self.handler.timeAwake()
		except:
			print ('Problem getting timeAwake')
	def killYourSelf(self, current = None):
		self.handler.killYourSelf()
	def getAttrList(self, current = None):
		try:
			return self.handler.getAttrList(self.communicator)
		except:
			print ('Problem getting getAttrList')
			traceback.print_exc()
			status = 1
			return



if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ic = Ice.initialize(sys.argv)
	status = 0
	mprx = {}
	try:

		# Remote object connection for DifferentialRobot
		try:
			proxyString = ic.getProperties().getProperty('DifferentialRobotProxy')
			try:
				basePrx = ic.stringToProxy(proxyString)
				differentialrobot_proxy = RoboCompDifferentialRobot.DifferentialRobotPrx.checkedCast(basePrx)
				mprx["DifferentialRobotProxy"] = differentialrobot_proxy
				print ("bien differential")
			except Ice.Exception:
				print ('Cannot connect to the remote object (DifferentialRobot)', proxyString)
				#traceback.print_exc()
				status = 1
		except Ice.Exception, e:
			print (e)
			print ('Cannot get DifferentialRobotProxy property.')
			status = 1


		# Remote object connection for Ultrasound
		try:
			proxyString = ic.getProperties().getProperty('UltrasoundProxy')
			try:
				basePrx = ic.stringToProxy(proxyString)
				ultrasound_proxy = RoboCompUltrasound.UltrasoundPrx.checkedCast(basePrx)
				mprx["UltrasoundProxy"] = ultrasound_proxy
				print ("bien ultrasound")
			except Ice.Exception:
				print ('Cannot connect to the remote object (Ultrasound)', proxyString)
				#traceback.print_exc()
				status = 1
		except Ice.Exception, e:
			print (e)
			print ('Cannot get UltrasoundProxy property.')
			status = 1

	except:
			traceback.print_exc()
			status = 1


	if status == 0:
		worker = SpecificWorker(mprx)


#		adapter.add(CommonBehaviorI(<LOWER>I, ic), ic.stringToIdentity('commonbehavior'))

		app.exec_()

	if ic:
		try:
			ic.destroy()
		except:
			traceback.print_exc()
			status = 1
