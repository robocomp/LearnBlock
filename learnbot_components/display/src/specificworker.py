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
from learnbot_components.display.src.genericworker import *

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel
configPath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'etc','config')

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		os.system("cat /home/pi/learnbot/learnbot_components/emotionalMotor/imgs/frameBuffer/Learnbot.fb > /dev/fb0")
		# self.timer.start(self.Period)

	def setParams(self, params):
		return True

	@QtCore.Slot()
	def compute(self):

		return True


	#
	# setImageFromFile
	#
	def setImageFromFile(self, pathImg):
		os.system("cat " + pathImg + " > /dev/fb0")
		pass


	#
	# setImage
	#
	def setImage(self, img):
		#
		#implementCODE
		#
		pass

