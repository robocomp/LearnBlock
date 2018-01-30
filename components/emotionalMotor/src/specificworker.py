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
#

import sys, os, traceback, time

from PySide import QtGui, QtCore
from genericworker import *

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		self.timer.start(self.Period)

	def setParams(self, params):
		#try:
		#	self.innermodel = InnerModel(params["InnerModelPath"])
		#except:
		#	traceback.print_exc()
		#	print "Error reading config params"
		return True

	@QtCore.Slot()
	def compute(self):

		return True

	def sendImage(file):
		img = QtGui.QImage(file)
		self.i+=1
		im = Image()
		im.Img=img.bits()
		im.width=img.width()
		im.height=img.height()
		try:
			self.display_proxy.setImage(im)
		except Exception as e:
			print e

	#
	# expressFear
	#
	def expressFear(self):
		self.display_proxy.setImageFromFile("/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/miedo.png")

	#
	# expressSurprise
	#
	def expressSurprise(self):
		self.display_proxy.setImageFromFile("/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/sorpresa.png")

	#
	# expressAnger
	#
	def expressAnger(self):
		self.display_proxy.setImageFromFile("/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/ira.png")

	#
	# expressSadness
	#
	def expressSadness(self):
		self.display_proxy.setImageFromFile("/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/tristeza.png")

	#
	# expressDisgust
	#
	def expressDisgust(self):
		self.display_proxy.setImageFromFile("/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/asco.png")

	#
	# expressJoy
	#
	def expressJoy(self):
		self.display_proxy.setImageFromFile("/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/alegria.png")
