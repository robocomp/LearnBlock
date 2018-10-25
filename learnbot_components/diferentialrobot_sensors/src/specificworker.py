#
# Copyright (C) 2015 by YOUR NAME HERE
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

# Import required Python libraries
from __future__ import print_function, absolute_import

import time
import RPi.GPIO as GPIO
import wiringpi2 as wpi

from PySide import *
from genericworker import *
from ultrasoundI import *
from differentialrobotI import *
import os, sys


class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		os.system('export LD_LIBRARY_PATH=/home/odroid/software/mjpg-streamer/mjpg-streamer')
		os.system('/home/odroid/software/mjpg-streamer/mjpg-streamer/./mjpg_streamer -i "input_uvc.so -y YUYV -r 320x240 -f 30 -d /dev/video0" -o "output_http.so -p 8080 -w /var/www" &')


		GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)

                GPIO.setup(6,GPIO.OUT)  # Direction Motor 1
                GPIO.setup(9,GPIO.OUT)  # Direction Motor 2
                GPIO.setup(23,GPIO.OUT)  # Trigger
		GPIO.setup(18,GPIO.OUT)  # LED Verde
                GPIO.setup(4,GPIO.OUT)  # LED Rojo
                GPIO.output(4,False)
		GPIO.output(18,True)
                GPIO.setup(17,GPIO.IN)      # Echo
                GPIO.setup(22,GPIO.IN)      # Echo
                GPIO.setup(24,GPIO.IN)      # Echo
                GPIO.setup(27,GPIO.IN)      # Echo

#################
#                self.ultrasound = {"sensor3": {"dist": 0, "angle":270, "GPIO-TRIGGER":23, "GPIO-ECHO":22}}
#                self.ultrasound = {"sensor0": {"dist": 0, "angle":180, "GPIO-TRIGGER":23, "GPIO-ECHO":24}}
#                self.ultrasound = {"sensor1": {"dist": 0, "angle":0, "GPIO-TRIGGER":23, "GPIO-ECHO":27}}
#                self.ultrasound = {"sensor2": {"dist": 0, "angle":90, "GPIO-TRIGGER":23, "GPIO-ECHO":17}}
################


                self.ultrasound = {"sensor0": {"dist": 0, "angle":180, "GPIO-TRIGGER":23, "GPIO-ECHO":24}, "sensor1": {"dist": 0, "angle":0, "GPIO-TRIGGER":23, "GPIO-ECHO":27}, "sensor2": {"dist": 0, "angle":90, "GPIO-TRIGGER":23, "GPIO-ECHO":17}, "sensor3": {"dist": 0, "angle":270, "GPIO-TRIGGER":23, "GPIO-ECHO":22}}


                self.adv = 0
		self.rot = 0
		wpi.wiringPiSetup()

		self.timer.timeout.connect(self.compute)
		self.Period = 3000
		self.timer.start(self.Period)


	def setParams(self, params):
		#// 	try
		#// 	{
		#// 		RoboCompCommonBehavior::Parameter par = params.at("InnerModelPath");
		#// 		innermodel_path=par.value;
		#// 		innermodel = new InnerModel(innermodel_path);
		#// 	}
		#// 	catch(std::exception e) { qFatal("Error reading config params"); }
		return True


	@QtCore.Slot()
	def compute(self):
#		print('SpecificWorker.compute...')
		#Ultrasound adquisition
		self.readUltrasound()
		return True


	def readUltrasound(self):
		# instead of physical pin numbers
		for nombre, sensor  in self.ultrasound.items():
			# Define GPIO to use on Pi
#                	GPIO_TRIGGER = sensor["GPIO-TRIGGER"]
			if (sensor.has_key("GPIO-TRIGGER") is True) and (sensor.has_key("GPIO-ECHO") is True):
				GPIO_TRIGGER = sensor["GPIO-TRIGGER"]
	                	GPIO_ECHO = sensor["GPIO-ECHO"]

        	        	# Set trigger to False (Low)
	        	        GPIO.output(GPIO_TRIGGER, False)

	        	        # Allow module to settle
        	        	time.sleep(0.1)

	        	        # Send 10us pulse to trigger
#				while True:
        	        	GPIO.output(GPIO_TRIGGER, True)
	                	time.sleep(0.00001)
		                GPIO.output(GPIO_TRIGGER, False)

     			        start = time.time()
                		while GPIO.input(GPIO_ECHO)==0:
		                  start = time.time()
				while GPIO.input(GPIO_ECHO)==1:
        		          stop = time.time()
				# Calculate pulse length
	                	elapsed = stop-start

	        	        # Distance pulse travelled in that time is time
        	        	# multiplied by the speed of sound (cm/s)
	                	distance = elapsed * 34000

		                # That was the distance there and back so halve the value
        		        distance = distance / 2
				sensor["dist"]=distance
		return True



	def computeRobotSpeed(self, vAdv, vRot):
		radius = 65 # milimetros
 		K = 11 # constante

		if (vRot == 0):
			vRot = 0.000000001
		Rrot = vAdv / (vRot * 0.7)
		Rl = Rrot - radius
		velLeft = vRot * Rl
		Rr = Rrot + radius
		velRight = vRot * Rr

#		return velLeft, velRight
		return velRight, velLeft

#########################################################################

	def getAllSensorData(self):
                return str(self.ultrasound)
#		print( self.SensorParamsList)
#		return (self.SensorParamsList)

	def getSensorData(self, sensor):

		if sensor in self.ultrasound.keys():
			return self.ultrasound[sensor]
		else:
			print("sheep")
			return {}

		ret = int()
		#
		# YOUR CODE HERE
		#
                # Use BCM GPIO references

		return ret

	def getBusParams(self):
		ret = BusParams()
		#
		# YOUR CODE HERE
		#
		return ret

#########################################################################

	def setSpeedBase(self, adv, rot):
		LEFT_PIN = 14
		RIGHT_PIN = 13

		wpi.pinMode(LEFT_PIN, 1)
    		wpi.pinMode(RIGHT_PIN, 1)


		velLeft, velRight = self.computeRobotSpeed(adv,rot)
		if (velLeft>=0):
			wpi.digitalWrite(LEFT_PIN, 0)
		else:
			wpi.digitalWrite(LEFT_PIN,1)
		time.sleep(0.1)
		if (velRight>=0):
			wpi.digitalWrite(RIGHT_PIN, 0)
		else:
			wpi.digitalWrite(RIGHT_PIN,1)
		time.sleep(0.1)

		fileWheelRight = open('/sys/devices/platform/pwm-ctrl/duty0','w')
		fileWheelRight.write(str(abs(velLeft)))
		fileWheelRight.close()
		fileWheelLeft = open('/sys/devices/platform/pwm-ctrl/duty1','w')
		fileWheelLeft.write(str(abs(velRight)))
		fileWheelLeft.close()

#		pass



	def correctOdometer(self, x, z, alpha):
                #
                # YOUR CODE HERE
                #
                pass

	def getBasePose(self):
                #
                # YOUR CODE HERE
                #
                x = int()
                z = int()
                alpha = float()
                return [x, z, alpha]
        def resetOdometer(self):
                #
                # YOUR CODE HERE
                #
                pass

        def setOdometer(self, state):
                #
                # YOUR CODE HERE
                #
                pass

        def getBaseState(self):
                #
                # YOUR CODE HERE
                #
                state = TBaseState()
                return state

        def setOdometerPose(self, x, z, alpha):
                #
                # YOUR CODE HERE
                #
                pass

        def stopBase(self):
                #
                # YOUR CODE HERE
                #
                pass

#        def setSpeedBase(self, adv, rot):
#		pass
