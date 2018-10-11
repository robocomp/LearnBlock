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

import sys, os, traceback, time

from PySide import QtGui, QtCore
from genericworker import *
import apriltag
import cv2
import numpy as np

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		# self.timer.timeout.connect(self.compute)
		# self.Period = 2000
		# self.timer.start(self.Period)
		self.detector = apriltag.Detector()
		self.cap = cv2.VideoCapture(0)
		while (True):
			# Capture frame-by-frame
			ret, frame = self.cap.read()

			# Our operations on the frame come here
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			aprils = self.detector.detect(gray)
			for a in aprils:
				print a.tag_id
				# tag = tag()
				# id = a.tag_id
				# tx =
				# ty =
				# tz =
				# rx =
				# ry =
				# rz =
				# ret.append(tag)
			# Display the resulting frame
			cv2.imshow('frame', gray)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

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
			frame = cv2.flip(frame, 0)
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
			aprils = self.detector.detect(frame)
			for a in aprils:
				tag = tag()
				id = a.tag_id
				# tx =
				# ty =
				# tz =
				# rx =
				# ry =
				# rz =
				ret.append(tag)
		except:
			print "Error Tag"
		return ret

