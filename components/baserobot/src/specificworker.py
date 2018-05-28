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
from pololu_drv8835_rpi import motors, MAX_SPEED


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min    

class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map):
        super(SpecificWorker, self).__init__(proxy_map)
        self.timer.timeout.connect(self.compute)
        self.Period = 2000
        motors.setSpeeds(0, 0)
        # self.timer.start(self.Period)

    def setParams(self, params):
        return True

    @QtCore.Slot()
    def compute(self):
        print ('SpecificWorker.compute...')
        self.setSpeedBase(0, 0)
        return True

    def computeRobotSpeed(self, vAdv, vRot):
        radius = 75 # milimetros
        K = 11 # constante

        if (vRot == 0):
            vRot = 0.000000001
        Rrot = vAdv / (vRot * 0.7)
        Rl = Rrot - radius
        velLeft = vRot * Rl
        Rr = Rrot + radius
        velRight = vRot * Rr
        velRight = map(velRight, -MAX_SPEED, MAX_SPEED,-300, 300)
        velLeft = map(velLeft, -MAX_SPEED, MAX_SPEED,-300, 300)
        if velRight > MAX_SPEED:
            velRight = MAX_SPEED
        if velLeft > MAX_SPEED:
            velLeft = MAX_SPEED
        return int(velLeft), int(velRight)


    def correctOdometer(self, x, z, alpha):
        pass


    def getBasePose(self):
        x = int()
        z = int()
        alpha = float()
        return [x, z, alpha]

    def resetOdometer(self):
        pass


    def setOdometer(self, state):
        pass


    def getBaseState(self):
        state = RoboCompGenericBase.TBaseState()
        return state


    def setOdometerPose(self, x, z, alpha):
        pass


    def stopBase(self):
        pass


    def setSpeedBase(self, adv, rot):
        velRight, velLeft = self.computeRobotSpeed(adv, rot)
        print ("Velocidad motores = ", velLeft, velRight)
        motors.setSpeeds(velLeft, velRight)
