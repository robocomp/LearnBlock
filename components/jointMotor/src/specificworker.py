#
# Copyright (C) 2018 by YOUR NAME HERE
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

import sys, os, traceback, time

from PySide import QtGui, QtCore
from genericworker import *
import wiringpi
from math  import pi


class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		self.timer.start(self.Period)
		wiringpi.wiringPiSetupGpio()
		wiringpi.pinMode(18,1)
		wiringpi.softPwmCreate(18,0,100)

	def setParams(self, params):
		return True

	@QtCore.Slot()
	def compute(self):
		print 'SpecificWorker.compute...'
		return True

	def Rad2OutPint(self, angle):
		if angle < -pi/2:
			angle = -pi/2
		elif angle > pi/2:
			angle = pi/2
		return (angle + pi/2) * (20 - 4) / (pi/2 + pi*2) + 4;

	def getAllMotorParams(self):
		ret = MotorParamsList()
		return ret

	def getAllMotorState(self):
		mstateMap = MotorStateMap()
		return mstateMap

	def getMotorParams(self, motor):
		ret = MotorParams()
		return ret

	def getMotorState(self, motor):
		ret = MotorState()
		return ret

	def setSyncVelocity(self, listGoals):
		pass

	def setZeroPos(self, name):
		pass

	def getBusParams(self):
		ret = BusParams()
		return ret

	def setSyncZeroPos(self):
		pass

	def setSyncPosition(self, listGoals):
		pass

	def getMotorStateMap(self, mList):
		ret = MotorStateMap()
		return ret

	def setPosition(self, goal):
		wiringpi.softPwmWrite(18, Rad2OutPint(goal))

	def setVelocity(self, goal):
		pass
