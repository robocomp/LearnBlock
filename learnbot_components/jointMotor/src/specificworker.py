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
from genericworker import *
import wiringpi
from math import pi
import Adafruit_PCA9685
configPath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'etc','config')

servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

def bezier(p1, p2, t):
	t = t / 10.
	diff = p2- p1
	return p1 + diff * t

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		# self.timer.start(self.Period)
		wiringpi.wiringPiSetupGpio()
		wiringpi.pinMode(18,1)
		wiringpi.softPwmCreate(18,0,100)
		wiringpi.softPwmWrite(18, 8)
		self.pwm = Adafruit_PCA9685.PCA9685()
		self.pwm.set_pwm_freq(60)
		self.oldAngle = int(self.Rad2OutPint(0))
		print ("Enviando angulo", self.oldAngle)
		self.pwm.set_pwm(7, 0, self.oldAngle)
	def setParams(self, params):
		return True

	@QtCore.Slot()
	def compute(self):
		print ('SpecificWorker.compute...')
		return True

	def Rad2OutPint(self, angle):
		angle = (angle + 0.6000000238) * (1.3 + 1.5) / (0.6000000238 + 0.6000000238) - 1.5
		if angle < -pi:
			angle = -pi
		elif angle > pi:
			angle = pi
		return (angle + pi) * (servo_max - servo_min) / (pi + pi) + servo_min;

	def getAllMotorParams(self):
		ret = MotorParamsList()
		return ret

	def getAllMotorState(self):
		mstateMap = MotorStateMap()
		return mstateMap

	def getMotorParams(self, motor):
		ret = MotorParams()
		return ret

	def getMotorState(self, motor):
		ret = MotorState()
		return ret

	def setSyncVelocity(self, listGoals):
		pass

	def setZeroPos(self, name):
		pass

	def getBusParams(self):
		ret = BusParams()
		return ret

	def setSyncZeroPos(self):
		pass

	def setSyncPosition(self, listGoals):
		pass

	def getMotorStateMap(self, mList):
		ret = MotorStateMap()
		return ret

	def setPosition(self, goal):
		new_angle = int(self.Rad2OutPint(goal.position))
		print ("Enviando angulo", new_angle)
		for t in range(10):
			angle = int(bezier(self.oldAngle, new_angle, t))
			self.pwm.set_pwm(7, 0, angle)
			time.sleep(0.05)
		self.oldAngle = new_angle
		# wiringpi.softPwmWrite(18, angle)
		# time.sleep(0.5)

	def setVelocity(self, goal):
		pass









# # Simple demo of of the PCA9685 PWM servo/LED controller library.
# # This will move channel 0 from min to max position repeatedly.
# # Author: Tony DiCola
# # License: Public Domain
# from __future__ import division
# import time
#
# # Import the PCA9685 module.
# import Adafruit_PCA9685
#
#
# # Uncomment to enable debug output.
# #import logging
# #logging.basicConfig(level=logging.DEBUG)
#
# # Initialise the PCA9685 using the default address (0x40).
# pwm = Adafruit_PCA9685.PCA9685()
#
# # Alternatively specify a different address and/or bus:
# #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
#
# # Configure min and max servo pulse lengths
# servo_min = 150  # Min pulse length out of 4096
# servo_max = 600  # Max pulse length out of 4096
#
# # Helper function to make setting a servo pulse width simpler.
# def set_servo_pulse(channel, pulse):
#     pulse_length = 1000000    # 1,000,000 us per second
#     pulse_length //= 60       # 60 Hz
#     print('{0}us per period'.format(pulse_length))
#     pulse_length //= 4096     # 12 bits of resolution
#     print('{0}us per bit'.format(pulse_length))
#     pulse *= 1000
#     pulse //= pulse_length
#     pwm.set_pwm(channel, 0, pulse)
#
# # Set frequency to 60hz, good for servos.
# pwm.set_pwm_freq(60)
#
# print('Moving servo on channel 0, press Ctrl-C to quit...')
# while True:
#     # Move servo on channel O between extremes.
#     pwm.set_pwm(15, 0, servo_min)
#     time.sleep(1)
#     pwm.set_pwm(15, 0, servo_max)
#     time.sleep(1)
