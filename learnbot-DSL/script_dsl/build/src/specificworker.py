
# Copyright (C) 2017 by Aniq Ur Rahman
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

import sys, os, Ice, traceback, time

from PySide import *
from genericworker import *

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except:
	print '$ROBOCOMP environment variable not set, using the default value /opt/robocomp'
	ROBOCOMP = '/opt/robocomp'
if len(ROBOCOMP)<1:
	print 'genericworker.py: ROBOCOMP environment variable not set! Exiting.'
	sys.exit()

preStr = "-I"+ROBOCOMP+"/interfaces/ --all "+ROBOCOMP+"/interfaces/"
Ice.loadSlice(preStr+"Laser.ice")
from RoboCompLaser import *
Ice.loadSlice(preStr+"DifferentialRobot.ice")
from RoboCompDifferentialRobot import *


class SpecificWorker(GenericWorker):


	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		self.timer.start(self.Period)
		self.ins_speed = 0
		self.ins_rot = 0
		self.ACTIVE = False
		self.isCorrect = False
		self.quit = False
		ipfile= open("src/commandset.txt", 'r')
		self.lines= ipfile.readlines()
		self.ncoms= len(self.lines)
		self.interpret= 0

	def setParams(self, params):
		return True

	# start of commands

	# STATE COMMANDS

	def start_bot(self):
		#The bot is activated
		self.ACTIVE = True
		print('~ Learbot activated')
		self.compute()

	def stop_bot(self):
		#The bot is stopped
		self.ACTIVE = False
		self.differentialrobot_proxy.setSpeedBase(0,0)
		print('~ Learbot stopped')
		self.ins_speed = 0
		self.ins_rot = 0
		self.compute()

	def halt_bot(self):
		self.differentialrobot_proxy.setSpeedBase(0,0)
		print('~ Learnbot halted')
		self.ins_speed = 0
		self.ins_rot = 0
		self.compute()

	# MOVE COMMANDS

	def move_right(self):
		#The bot turns right and moves staright
		print('~ Turning right...')
		if self.ins_speed < 0:
			self.ins_speed = -self.ins_speed
		if self.ins_speed == 0:
			self.ins_speed = 100
		self.ins_rot = 1.5707
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(1)
		self.move_straight()

	def move_left(self):
		#The bot turns left and moves staright
		print('~ Turning left...')
		if self.ins_speed < 0:
			self.ins_speed = -self.ins_speed
		if self.ins_speed == 0:
			self.ins_speed = 100
		self.ins_rot = -1.5707
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(1)
		self.move_straight()

	def move_straight(self):
		#The bot moves staright
		print('~ Moving straight...')
		if self.ins_speed < 0:
			self.ins_speed = -self.ins_speed
		if self.ins_speed == 0:
			self.ins_speed = 100
		self.ins_rot = 0
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(1)
		self.compute()

	def move_back(self):
		#The bot turns backward, with front still facing forward
		print('~ Moving back...')
		if self.ins_speed > 0:
			self.ins_speed = -self.ins_speed
		if self.ins_speed == 0:
			self.ins_speed = -100
		self.ins_rot = 0
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(1)
		self.compute()

	# MOVE COMMANDS DISTANCE SUPPLIED

	def move_right_dist(self, dist):
		#The bot turns right and moves staright
		print('~ Turning right...')
		if self.ins_speed < 0:
			self.ins_speed = -self.ins_speed
		if self.ins_speed == 0:
			self.ins_speed = 100
		self.ins_rot = 1.5707
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(1)
		self.move_straight_dist(dist)

	def move_left_dist(self, dist):
		#The bot turns left and moves staright
		print('~ Turning left...')
		if self.ins_speed < 0:
			self.ins_speed = -self.ins_speed
		if self.ins_speed == 0:
			self.ins_speed = 100
		self.ins_rot = -1.5707
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(1)
		self.move_straight_dist(dist)

	def move_straight_dist(self, dist):
		#The bot moves staright
		print('~ Moving straight...')
		if self.ins_speed < 0:
			self.ins_speed = -self.ins_speed
		if self.ins_speed == 0:
			self.ins_speed = 100
		self.ins_rot = 0
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(dist/self.ins_speed)
		self.halt_bot()

	def move_back_dist(self, dist):
		#The bot turns backward, with front still facing forward
		print('~ Moving back...')
		if self.ins_speed > 0:
			self.ins_speed = -self.ins_speed
		if self.ins_speed == 0:
			self.ins_speed = -100
		self.ins_rot = 0
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(-dist/self.ins_speed)
		self.halt_bot()

	# TURN COMMANDS

	def turn_back(self):
		print('~ Turning back...')
		#Code to make the bot turn 180 degrees
		self.ins_rot = 3.14
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(1)
		print('~ The bot has turned back')
		self.halt_bot()

	def turn_left(self):
		print('~ Turning left...')
		#Code to make the bot turn 90 degrees left
		self.ins_rot = -1.5707
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(1)
		print('~ The bot has turned left')
		self.halt_bot()

	def turn_right(self):
		print('~ Turning right...')
		#Code to make the bot turn 90 degrees right
		self.ins_rot = 1.5707
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(1)
		print('~ The bot has turned right')
		self.halt_bot()

	def turn(self, angle):
		print('~ Turning...')
		#Code to make the bot turn by angle degrees
		self.ins_rot= float(angle*3.14/180)
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, self.ins_rot)
		time.sleep(1)
		print('~ The bot has rotated ' + str(angle) + ' degrees')
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, 0)
		self.ins_rot = 0
		self.compute()


	# SET AND GET COMMANDS

	def set_speed(self, adv):
		#Sets the speed of the Learnbot
		self.differentialrobot_proxy.setSpeedBase(adv, self.ins_rot)
		print('~ The Speed is set to ' + str(adv))
		self.ins_speed = adv
		self.compute()

	def set_rot(self, rot):
		#Sets the angualar speed of the Learnbot
		self.differentialrobot_proxy.setSpeedBase(self.ins_speed, rot)
		print('~ The Angular Speed is set to ' + str(rot))
		self.compute()

	def get_speed(self):
		print('~ The Speed is ' + str(self.ins_speed))
		self.compute()

	def get_rot(self):
		print('~ The Angular Speed is ' + str(self.ins_rot))
		self.compute()

	def get_position():
		#Displays the coordinates of the Learnbot wrt the starting position
		#DUMMY
		print('~ X: <x_val>  Y: <y_val> ')
		self.compute()

	def set_origin():
		#Sets the current position as origin and resets the coordinates to (0,0)
		#DUMMY
		print('~ The origin is reset')
		self.compute()

	# end of commands

	@QtCore.Slot()
	def compute(self):
		# print 'SpecificWorker.compute...'
		try:
		
			while self.quit is False:
				command = self.lines[self.interpret]
				self.interpret= self.interpret + 1
				# command = raw_input('>>>  ')
				self.isCorrect = False
				pcom = command.strip().split(' ')
				comlen = len(pcom)
				#This technique makes the interpretation of the conditional block faster

				if pcom[0] == 'start':
					self.start_bot()
					self.isCorrect = True

				if self.ACTIVE == False:
					print('~ Learnbot is not active, type start to activate it')
					self.isCorrect = True

				if self.ACTIVE is True:
					
					if comlen == 1:
						if pcom[0] == 'stop':
							self.stop_bot()
							self.isCorrect = True
						if pcom[0] == 'halt':
							self.halt_bot()
							self.isCorrect = True
						if pcom[0] == 'restart':
							self.restart_bot()
							self.ACTIVE = True
							self.isCorrect = True
						if pcom[0] == 'right':
							self.move_right()
							self.isCorrect = True
						if pcom[0] == 'left':
							self.move_left()
							self.isCorrect = True
						if pcom[0] == 'back':
							self.move_back()
							self.isCorrect = True
						if pcom[0] == 'straight':
							self.move_straight()
							self.isCorrect = True

					if comlen == 2:
						if pcom[0] == 'right':
							self.move_right_dist(int(pcom[1]))
							self.isCorrect = True
						if pcom[0] == 'left':
							self.move_left_dist(int(pcom[1]))
							self.isCorrect = True
						if pcom[0] == 'back':
							self.move_back_dist(int(pcom[1]))
							self.isCorrect = True
						if pcom[0] == 'straight':
							self.move_straight_dist(int(pcom[1]))
							self.isCorrect = True
						if pcom[0] == 'continue':
							time.delay(int(pcom[1]))
						if pcom[0] == 'turn' and pcom[1] == 'back':
							self.turn_back()
							self.isCorrect = True
						if pcom[0] == 'turn' and pcom[1] == 'left':
							self.turn_left()
							self.isCorrect = True
						if pcom[0] == 'turn' and pcom[1] == 'right':
							self.turn_right()
							self.isCorrect = True
						if pcom[0] == 'reset' and pcom[1] == 'xy':
							self.set_origin()
							self.isCorrect = True
						if pcom[0] == 'turn':
							self.turn(float(pcom[1]))
							self.isCorrect = True
						if pcom[0] == 'delay':
							time.sleep(int(pcom[1]))
							self.isCorrect = True

					if comlen == 3:
						if pcom[0] == 'what' and pcom[1] == 'is' and pcom[2] == 'xy':
							self.get_position()
							self.isCorrect = True
						if pcom[0] == 'what' and pcom[1] == 'is' and pcom[2] == 'speed':
							self.get_speed()
							self.isCorrect = True
						if pcom[0] == 'what' and pcom[1] == 'is' and pcom[2] == 'rotation':
							self.get_rot()
							self.isCorrect = True

					if comlen == 4:
						if pcom[0] == 'set' and pcom[1] == 'speed' and pcom[2] == 'to':
							self.set_speed(float(pcom[3]))
							self.isCorrect = True
						if pcom[0] == 'set' and pcom[1] == 'rotation' and pcom[2] == 'to':
							self.set_rot(float(pcom[3]))
							self.isCorrect = True

				if pcom[0] == 'quit' or pcom[0] == 'exit':
					print('~ Quiting terminal...')
					self.isCorrect = True
					self.quit= True
					sys.exit()
					
				if self.isCorrect is False:
					print('~ Sorry! The command does not exist.')

		except Ice.Exception, e:
				traceback.print_exc()
				print e
		return True