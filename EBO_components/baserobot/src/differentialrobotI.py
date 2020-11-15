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
	print('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
	ROBOCOMP = '/opt/robocomp'
if len(ROBOCOMP)<1:
	print('ROBOCOMP environment variable not set! Exiting.')
	sys.exit()

from EBO_components import pathInterfaces
ice_DifferentialRobot = False
if os.path.isfile(os.path.join(pathInterfaces, 'DifferentialRobot.ice')):
	wholeStr = "-I" + pathInterfaces + " --all "+os.path.join(pathInterfaces, 'DifferentialRobot.ice')
	Ice.loadSlice(wholeStr)
	ice_DifferentialRobot = True


if not ice_DifferentialRobot:
	print('Couldn\'t load DifferentialRobot')
	sys.exit(-1)
from RoboCompDifferentialRobot import *

class DifferentialRobotI(DifferentialRobot):
	def __init__(self, worker):
		self.worker = worker

	def correctOdometer(self, x, z, alpha, c):
		return self.worker.correctOdometer(x, z, alpha)
	def getBasePose(self, c):
		return self.worker.getBasePose()
	def resetOdometer(self, c):
		return self.worker.resetOdometer()
	def setOdometer(self, state, c):
		return self.worker.setOdometer(state)
	def getBaseState(self, c):
		return self.worker.getBaseState()
	def setOdometerPose(self, x, z, alpha, c):
		return self.worker.setOdometerPose(x, z, alpha)
	def stopBase(self, c):
		return self.worker.stopBase()
	def setSpeedBase(self, adv, rot, c):
		return self.worker.setSpeedBase(adv, rot)
