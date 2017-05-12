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
Ice.loadSlice(preStr+"Ultrasound.ice")
from RoboCompUltrasound import *
Ice.loadSlice(preStr+"DifferentialRobot.ice")
from RoboCompDifferentialRobot import *


from ultrasoundI import *
from differentialrobotI import *


try:
	import wiringpi2 as wpi
except ImportError:
	print "Wiring pi not found. Please, download and install"
	print "Odroid: https://github.com/hardkernel/wiringPi" 
	print "Raspberry: http://wiringpi.com/download-and-install"
	exit()


class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 3000
		self.timer.start(self.Period)

		#os.system('/home/odroid/software/mjpg-streamer/mjpg-streamer/./mjpg_streamer -i "input_uvc.so -y YUYV -r 320x240 -f 30 -d /dev/video0" -o "output_http.so -p 8080 -w /var/www" &')
		os.system('sbin/./launch_learnbot.sh')
		time.sleep(2)

		# Initialize the sonar.
		wpi.pinMode(4, 1) #trigger
		for id_pin in [0,2,3,50]: # echos
			wpi.pinMode(id_pin, 0)

		self.sonar_values = {"sensor0": {"dist": 0, "angle":180, "PIN-TRIGGER":4, "PIN-ECHO":5},\
							"sensor1": {"dist": 0, "angle":0, "PIN-TRIGGER":4, "PIN-ECHO":2},\
							"sensor2": {"dist": 0, "angle":90, "PIN-TRIGGER":4, "PIN-ECHO":0},\
							"sensor3": {"dist": 0, "angle":270, "PIN-TRIGGER":4, "PIN-ECHO":3}}
		self.left_wheel_pin  = 14
		self.right_wheel_pin = 13


	def show_pin_conections(self):
		print "TRIGER_PIN = 1"
		print "ECHO_SENSOR_1 = 5"
		print "ECHO_SENSOR_2 = 2"
		print "ECHO_SENSOR_3 = 0"
		print "ECHO_SENSOR_4 = 3"
		print "PINOUT: http://www.hardkernel.com/main/products/prdt_info.php?g_code=G143703355573&tab_idx=2"


	def read_ultrasound(self):
		# instead of physical pin numbers
		for _, sensor  in self.ultrasound.items():
			if (sensor.has_key("PIN-TRIGGER")) and (sensor.has_key("PIN-ECHO")):
				PIN_TRIGGER = sensor["PIN-TRIGGER"]
				PIN_ECHO = sensor["PIN-ECHO"]

				# Set trigger to False (Low)
				wpi.digitalWrite(PIN_TRIGGER, 0)
				# Allow module to settle
				time.sleep(0.1)

				# Send 10us pulse to trigger
				wpi.digitalWrite(PIN_TRIGGER, 1)
				time.sleep(0.00001)
				wpi.digitalWrite(PIN_TRIGGER, 0)
	
				time_start = time.time()
				while wpi.digitalRead(PIN_ECHO) == 0:
					start = time.time()
					if (time_start - start > 3000):
						start = -1
						break
				if start == -1:
					print "WARNING", "PIN_TRIGGER:",PIN_TRIGGER, "not work!"
					sensor["dist"] = -1
				else:
					while wpi.digitalRead(GPIO_ECHO) == 1:
						stop = time.time()
						if (stop - start > 3000):
							stop = -1
							break
					if stop == -1:
						print "WARNING", "PIN_ECHO:",PIN_ECHO, "not work!"
						sensor["dist"] = -1
					else:
						# Calculate pulse length
						elapsed = stop-start
						# Distance pulse travelled in that time is time
						# multiplied by the speed of sound (cm/s)
						distance = elapsed * 34000
						# That was the distance there and back so halve the value
						sensor["dist"] = distance / 2.
		return True	


	@QtCore.Slot()
	def compute(self):
		print "working!"
		read_ultrasound()


	def compute_robot_speed(self, vAdv, vRot):
		radius = 65 # milimetros
 		#K = 11 # constant
 		m = 0.7 # constant to adapt reducer of motor
 		
		vRot = 1e-30 if (vRot == 0) else vRot # correct vrot minimal when not rotation
		Rrot = vAdv / (vRot * m)
		velRight = vRot * (Rrot + radius)
		velLeft = vRot * (Rrot - radius)

		return velLeft, velRight


	def getAllSensorDistances(self):
		return str(self.sonar_values)


	def getSensorDistance(self, sensor_id):
		if sensor_id in self.ultrasound.keys():
			return self.sonar_values[sensor_id]	
		else:
			print "not sensor locate!"
			return {}


	def stopBase(self):
		for id_duty in range(2):
			with open('/sys/devices/platform/pwm-ctrl/duty'+str(id_duty), 'w') as file_duty:
				file_duty.write(str(0))


	def setSpeedBase(self, adv, rot):
		wpi.pinMode(self.leftt_wheel_pin, 1)
		wpi.pinMode(self.right_wheel_pin, 1)

		velLeft, velRight = self.computeRobotSpeed(adv,rot)

		for pin, speed in zip([self.left_wheel_pin, self.right_wheel_pin], [velLeft,velRight]):
			direction = 0 if (speed >= 0) else 1
			wpi.digitalWrite(pin, direction)
			time.sleep(0.1)

		for id_duty, speed in zip(range(2), [self.left_wheel_pin, self.right_wheel_pin]):
			with open('/sys/devices/platform/pwm-ctrl/duty'+str(id_duty), 'w') as file_duty:
				file_duty.write(str(abs(speed)))



