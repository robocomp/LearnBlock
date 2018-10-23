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

import sys, os, Ice

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except:
	print ('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
	ROBOCOMP = '/opt/robocomp'
if len(ROBOCOMP)<1:
	print ('ROBOCOMP environment variable not set! Exiting.')
	sys.exit()

from learnbot_components import pathInterfaces
ice_JointMotor = False
if os.path.isfile(os.path.join(pathInterfaces,+'JointMotor.ice')):
	wholeStr = "-I" + pathInterfaces + " --all "+os.path.join(pathInterfaces,+'JointMotor.ice')
	Ice.loadSlice(wholeStr)
	ice_JointMotor = True

if not ice_JointMotor:
	print ('Couldn\'t load JointMotor')
	sys.exit(-1)
from RoboCompJointMotor import *

class JointMotorI(JointMotor):
	def __init__(self, worker):
		self.worker = worker

	def getAllMotorParams(self, c):
		return self.worker.getAllMotorParams()
	def getAllMotorState(self, c):
		return self.worker.getAllMotorState()
	def getMotorParams(self, motor, c):
		return self.worker.getMotorParams(motor)
	def getMotorState(self, motor, c):
		return self.worker.getMotorState(motor)
	def setSyncVelocity(self, listGoals, c):
		return self.worker.setSyncVelocity(listGoals)
	def setZeroPos(self, name, c):
		return self.worker.setZeroPos(name)
	def getBusParams(self, c):
		return self.worker.getBusParams()
	def setSyncZeroPos(self, c):
		return self.worker.setSyncZeroPos()
	def setSyncPosition(self, listGoals, c):
		return self.worker.setSyncPosition(listGoals)
	def getMotorStateMap(self, mList, c):
		return self.worker.getMotorStateMap(mList)
	def setPosition(self, goal, c):
		return self.worker.setPosition(goal)
	def setVelocity(self, goal, c):
		return self.worker.setVelocity(goal)
