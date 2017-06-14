#
# Copyright (C) 2017 by YOUR NAME HERE
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
from PySide import *

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
	print '$ROBOCOMP environment variable not set, using the default value /opt/robocomp'
	ROBOCOMP = '/opt/robocomp'

preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"
Ice.loadSlice(preStr+"CommonBehavior.ice")
import RoboCompCommonBehavior

preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"
Ice.loadSlice(preStr+"DifferentialRobot.ice")
from RoboCompDifferentialRobot import *
preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"
Ice.loadSlice(preStr+"GenericBase.ice")
from RoboCompGenericBase import *
preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"
Ice.loadSlice(preStr+"Laser.ice")
from RoboCompLaser import *
preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"
Ice.loadSlice(preStr+"GenericBase.ice")
from RoboCompGenericBase import *
preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"
Ice.loadSlice(preStr+"RGBD.ice")
from RoboCompRGBD import *
preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"
Ice.loadSlice(preStr+"JointMotor.ice")
from RoboCompJointMotor import *
preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"
Ice.loadSlice(preStr+"GenericBase.ice")
from RoboCompGenericBase import *



try:
	from ui_mainUI import *
except:
	print "Can't import UI file. Did you run 'make'?"
	sys.exit(-1)


class GenericWorker(QtGui.QWidget):
	kill = QtCore.Signal()


	def __init__(self, mprx):
		super(GenericWorker, self).__init__()


		self.differentialrobot_proxy = mprx["DifferentialRobotProxy"]
		self.laser1_proxy = mprx["LaserProxy1"]
		self.laser2_proxy = mprx["LaserProxy2"]
		self.laser3_proxy = mprx["LaserProxy3"]
		self.laser4_proxy = mprx["LaserProxy4"]
		self.rgbd_proxy = mprx["RGBDProxy"]
		self.ui = Ui_guiDlg()
		self.ui.setupUi(self)
		self.show()
		
		
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
		print "Period changed", p
		Period = p
		timer.start(Period)
