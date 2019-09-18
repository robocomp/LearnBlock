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
from __future__ import print_function, absolute_import

import sys, os, Ice
#ROBOCOMP = ''
#try:
#	ROBOCOMP = os.environ['ROBOCOMP']
#except:
#	print('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
#	ROBOCOMP = '/opt/robocomp'
#if len(ROBOCOMP)<1:
#	print('ROBOCOMP environment variable not set! Exiting.')
#	sys.exit()

additionalPathStr = ''
icePaths = [os.path.dirname(__file__)]
ice_Apriltag = False
for p in icePaths:
	if os.path.isfile(p+'/Apriltag.ice'):
		preStr = "-I" + p + " --all " + p + '/'
		wholeStr = preStr+"Apriltag.ice"
		Ice.loadSlice(wholeStr)
		ice_Apriltag = True
		break
if not ice_Apriltag:
	print('Couldn\'t load Apriltag')
	sys.exit(-1)
from RoboCompApriltag import *

class ApriltagI(Apriltag):
	def __init__(self, worker):
		self.worker = worker

	def processimage(self, frame, c):
		return self.worker.processimage(frame)
