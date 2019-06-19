#
# Copyright (C) 2019 by YOUR NAME HERE
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
		print 'SpecificWorker.compute...'
		#computeCODE
		#try:
		#	self.differentialrobot_proxy.setSpeedBase(100, 0)
		#except Ice.Exception, e:
		#	traceback.print_exc()
		#	print e

		# The API of python-innermodel is not exactly the same as the C++ version
		# self.innermodel.updateTransformValues("head_rot_tilt_pose", 0, 0, 0, 1.3, 0, 0)
		# z = librobocomp_qmat.QVec(3,0)
		# r = self.innermodel.transform("rgbd", z, "laser")
		# r.printvector("d")
		# print r[0], r[1], r[2]

		return True

	def ponerEsp(self):
	    voices  = self.engine.getProperty('voices')
	    idvoice = 0

	    for voice in voices:
		idvoice+=1
		if voice.id == 'spanish':
		        print("void ID: ", voice.id)
			self.engine.setProperty('voice', voice.id)
			self.engine.say("Definido el lenguaje")
			self.engine.runAndWait()

	def prueba(self):
		frase = 'Me gustan las casas con las paredes azules y el tejado verde'
		self.engine.setProperty('rate', 180)
		self.engine.setProperty('voice', 'spanish+f6')
		self.engine.say(frase)
		self.engine.setProperty('voice', 'spanish+f1')
		self.engine.say(frase)
		self.engine.setProperty('voice', 'spanish+f2')
		self.engine.say(frase)
		self.engine.setProperty('voice', 'spanish+f3')
		self.engine.say(frase)
		self.engine.setProperty('voice', 'spanish+f4')
		self.engine.say(frase)
		self.engine.setProperty('voice', 'spanish+f5')
		self.engine.say(frase)

	#
	# say
	#
	def say(self, text):
		import pyttsx3
		self.engine = pyttsx3.init()
		#self.ponerEsp()
		self.prueba()
		#self.engine.say(text)	
		self.engine.runAndWait()
		self.engine.stop()
		pass

