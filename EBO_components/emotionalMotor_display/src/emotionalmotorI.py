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
ice_EmotionalMotor = False
if os.path.isfile(os.path.join(pathInterfaces, 'EmotionalMotor.ice')):
	wholeStr = "-I" + pathInterfaces + " --all "+os.path.join(pathInterfaces, 'EmotionalMotor.ice')
	Ice.loadSlice(wholeStr)
	ice_EmotionalMotor = True

if not ice_EmotionalMotor:
	print('Couldn\'t load EmotionalMotor')
	sys.exit(-1)
from RoboCompEmotionalMotor import *
ice_Display = False
for p in [pathInterfaces]:
	if os.path.isfile(p+'/Display.ice'):
		preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ " + " --all "+p+'/'
		wholeStr = preStr+"Display.ice"
		Ice.loadSlice(wholeStr)
		ice_Display = True
		break
if not ice_Display:
	print('Couldn\'t load Display')
	sys.exit(-1)
from RoboCompDisplay import *

class EmotionalMotorI(EmotionalMotor):
	def __init__(self, worker):
		self.worker = worker

	def expressFear(self, c):
		return self.worker.expressFear()
	def expressSurprise(self, c):
		return self.worker.expressSurprise()
	def expressAnger(self, c):
		return self.worker.expressAnger()
	def expressSadness(self, c):
		return self.worker.expressSadness()
	def expressNeutral(self, c):
		return self.worker.expressNeutral()
	def expressDisgust(self, c):
		return self.worker.expressDisgust()
	def expressJoy(self, c):
		return self.worker.expressJoy()
