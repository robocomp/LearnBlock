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

import sys, os, traceback, time, threading

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
		self.Period = 0
		self.timer.start(self.Period)
		self.scene = QtGui.QGraphicsScene()
		self.image = None
		self.item_pixmap = None
		self.changeImage = False
		self.mutex = threading.RLock()
		self.showFullScreen()
		self.imagePath=None

	def setParams(self, params):
		self.ui.graphic.setScene(self.scene)
		self.ui.graphic.show()
		return True

	@QtCore.Slot()
	def compute(self):
		self.mutex.acquire()
		try:
			if self.changeImage:
				print ("cargando imagen", self.imagePath)
				# self.pixmap = QtGui.QPixmap.fromImage(self.image)
				self.pixmap = QtGui.QPixmap(self.imagePath)
				if self.item_pixmap is None:
					self.item_pixmap = self.scene.addPixmap(self.pixmap)
				else:
					self.item_pixmap.setPixmap(self.pixmap)
				self.changeImage = False
		except:
			traceback.print_exc()
		finally:
			self.mutex.release()
		return True

	#
	# setImageFromFile
	#
	def setImageFromFile(self, pathImg):
		print ("setImageFromFile")
		self.mutex.acquire()
		try:
			self.changeImage = True
			self.imagePath=pathImg
		except:
			traceback.print_exc()
		finally:
			self.mutex.release()

	#
	# setImage
	#
	def setImage(self, img):
		self.mutex.acquire()
		try:
			self.changeImage = True
			self.image = QtGui.QImage(img.Img,img.width,img.height, QtGui.QImage.Format_ARGB32)
			self.image.save("tmp.png")
			self.imagePath="tmp.png"
		except:
			traceback.print_exc()
		finally:
			self.mutex.release()
