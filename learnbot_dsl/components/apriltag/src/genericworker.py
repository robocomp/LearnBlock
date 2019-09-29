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
from __future__ import print_function, absolute_import

import sys, Ice, os
from PySide2 import QtGui, QtCore

#ROBOCOMP = ''
#try:
#	ROBOCOMP = os.environ['ROBOCOMP']
#except KeyError:
#	print('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
#	ROBOCOMP = '/opt/robocomp'

from learnbot_dsl import PATHINTERFACES as pathInterfaces

if os.path.isfile(os.path.join(pathInterfaces, 'CommonBehavior.ice')):
	wholeStr = "-I" + pathInterfaces + " --all "+os.path.join(pathInterfaces, 'CommonBehavior.ice')
	Ice.loadSlice(wholeStr)


#preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"
#Ice.loadSlice(preStr+"CommonBehavior.ice")
import RoboCompCommonBehavior

additionalPathStr = ''
icePaths = [ os.path.dirname(__file__)]

print(icePaths)
ice_Apriltag = False
for p in icePaths:
	if os.path.isfile(p+'/Apriltag.ice'):
		preStr = "-I" + p + " --all " + p + '/'
		wholeStr = preStr+"Apriltag.ice"
		print(wholeStr)
		Ice.loadSlice(wholeStr)
		ice_Apriltag = True
		break
if not ice_Apriltag:
	print('Couln\'t load Apriltag')
	sys.exit(-1)
from RoboCompApriltag import *


from learnbot_dsl.components.apriltag.src.apriltagI import *


class GenericWorker(QtCore.QObject):
	kill = QtCore.Signal()


	def __init__(self, mprx):
		super(GenericWorker, self).__init__()




		self.mutex = QtCore.QMutex(QtCore.QMutex.Recursive)
		self.Period = 30
		self.timer = QtCore.QTimer(self)


	@QtCore.Slot()
	def killYourSelf(self):
		rDebug("Killing myself")
		self.kill.emit()

	# \brief Change compute period
	# @param per Period in ms
	@QtCore.Slot(int)
	def setPeriod(self, p):
		print("Period changed", p)
		Period = p
		timer.start(Period)
