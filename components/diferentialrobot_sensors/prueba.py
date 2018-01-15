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
import time
import wiringpi2 as wpi

import os, sys







def computeRobotSpeed(self, vAdv, vRot):
		radius = 65 # milimetros
 		K = 11 # constante
		leftSwitch = 1
		rightSwitch = 1

		if (vRot == 0):
			vRot = 0.000000001
		Rrot = vAdv / vRot
		Rl = Rrot - radius
		velLeft = vRot * Rl
		Rr = Rrot + radius
		velRight = vRot * Rr

		# Computar el sentido del giro
		if (velRight<0):
				rightSwitch = 0
				velRight *= -1
		if (velLeft<0):
				leftSwitch = 0
				velLeft *= -1

		# Filtramos el valor para que este en los margenes del pwm del motor
		if(velRight>1024):
				velRight=1024
		if(velLeft>1024):
				velLeft=1024

###################################################################################
		return velLeft, leftSwitch, velRight, rightSwitch



#########################################################################

leftSwitch=1
dutyLeft=0
rightSwitch=1
dutyRight=0


# IO ports of the left motor
LEFT_ENABLE = '/sys/devices/platform/pwm-ctrl/enable0'
LEFT_DUTY   = '/sys/devices/platform/pwm-ctrl/duty0'
LEFT_FREQ   = '/sys/devices/platform/pwm-ctrl/freq0'
LEFT_PIN = 14
 
# IO ports of the right motor
RIGHT_ENABLE = '/sys/devices/platform/pwm-ctrl/enable1'
RIGHT_DUTY   = '/sys/devices/platform/pwm-ctrl/duty1'
RIGHT_FREQ   = '/sys/devices/platform/pwm-ctrl/freq1'
RIGHT_PIN = 13

if (leftSwitch==0):
	wpi.digitalWrite(LEFT_PIN, 0)
else:
	wpi.digitalWrite(LEFT_PIN,1)

time.sleep(0.1)
if (rightSwitch==0):
	wpi.digitalWrite(RIGHT_PIN, 1)
else:
	wpi.digitalWrite(RIGHT_PIN,0)

time.sleep(0.1)

fileWheelRight = open('/sys/devices/platform/pwm-ctrl/duty0','w')
fileWheelRight.write(str(dutyLeft))
fileWheelRight.close()
fileWheelLeft = open('/sys/devices/platform/pwm-ctrl/duty1','w')
fileWheelLeft.write(str(dutyRight))
fileWheelLeft.close()

#		pass

