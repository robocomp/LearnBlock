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

import sys, Ice, os
from PySide2 import QtGui, QtCore

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
	print ('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
	ROBOCOMP = '/opt/robocomp'

preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all "+ROBOCOMP+"/interfaces/" #/home/pi/learnbot/interfaces/"
Ice.loadSlice(preStr+"CommonBehavior.ice")
import RoboCompCommonBehavior

pathInterfaces = os.path.join(os.path.dirname(__file__),'../../interfaces')
additionalPathStr = ""
icePaths = [ '/home/pi/learnbot/interfaces/', pathInterfaces]
try:
	SLICE_PATH = os.environ['SLICE_PATH'].split(':')
	for p in SLICE_PATH:
		icePaths.append(p)
		additionalPathStr += ' -I' + p + ' '
	icePaths.append('/opt/robocomp/interfaces')
except:
	print ('SLICE_PATH environment variable was not exported. Using only the default paths')
	pass

ice_EmotionalMotor = False
for p in icePaths:
	if os.path.isfile(p+'/EmotionalMotor.ice'):
		preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ " + additionalPathStr + " --all "+p+'/'
		wholeStr = preStr+"EmotionalMotor.ice"
		Ice.loadSlice(wholeStr)
		ice_EmotionalMotor = True
		break
if not ice_EmotionalMotor:
	print ('Couln\'t load EmotionalMotor')
	sys.exit(-1)
from RoboCompEmotionalMotor import *
ice_Display = False
for p in icePaths:
	if os.path.isfile(p+'/Display.ice'):
		preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ " + additionalPathStr + " --all "+p+'/'
		wholeStr = preStr+"Display.ice"
		Ice.loadSlice(wholeStr)
		ice_Display = True
		break
if not ice_Display:
	print ('Couln\'t load Display')
	sys.exit(-1)
from RoboCompDisplay import *


from emotionalmotorI import *


class GenericWorker(QtCore.QObject):
	kill = QtCore.Signal()


	def __init__(self, mprx):
		super(GenericWorker, self).__init__()


		self.display_proxy = mprx["DisplayProxy"]


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
		print ("Period changed", p)
		Period = p
		timer.start(Period)
