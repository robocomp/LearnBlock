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
#    but WITHOUT ANY WARRANTY without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import print_function, absolute_import

import sys, os, traceback, time
from PySide2 import QtGui, QtCore
from learnbot_dsl.components.apriltag.src.genericworker import *
import apriltag
import cv2
import numpy as np
configPath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'etc','config')
class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.detector = apriltag.Detector()

	def setParams(self, params):
		return True

	@QtCore.Slot()
	def compute(self):

		return True

	#
	# processimage
	#
	def processimage(self, frame):
		ret=[]
		try:
			arr = np.fromstring(frame.image, np.uint8)
			frame = np.reshape(arr, (frame.width, frame.height, frame.depth))
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			#frame = cv2.flip(frame, 0)
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
			aprils = self.detector.detect(frame)
			#print(aprils)
			for a in aprils:
				Tag = tag()
				Tag.id = a.tag_id
				Tag.cx = a.center[0]
				Tag.cy = a.center[1]
				# tx =
				# ty =
				# tz =
				# rx =
				# ry =
				# rz =
				ret.append(Tag)
		except Exception as e:
			traceback.print_exc()
			print("Error Tag")
		return ret

