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

import Adafruit_PCA9685, threading

from learnbot_components.laser.src.genericworker import *
import learnbot_components.laser.src.VL53L0X as VL53L0X, time
configPath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'etc','config')

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
        self.mutex = threading.Lock()
        pinSensors = [(11, 0x20), (13, 0x21), (12, 0x22), (14, 0x23), (15, 0x24)]
        pwm = Adafruit_PCA9685.PCA9685()
        self.tofs = []
        for pin, address in pinSensors:
                pwm.set_pwm(pin, 0, 4096)

        for pin, address in pinSensors:
                tof = VL53L0X.VL53L0X(address=address)
                pwm.set_pwm(pin, 4096, 0)
                time.sleep(0.50)
                tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
                self.tofs.append(tof)
                self.timing = tof.get_timing()

        self.laserData = []
        self.mutex.acquire()
        for tof in self.tofs:
                data = TData()
                data.dist = tof.get_distance()
                data.angle = tof.my_object_number
                self.laserData.append(data)
        self.mutex.release()
        self.timer.start(self.timing/1000)

    def setParams(self, params):
        return True

    @QtCore.Slot()
    def compute(self):
        self.mutex.acquire()
        self.laserData = []
        for tof in self.tofs:
                data = TData()
                data.dist = tof.get_distance()
                data.angle = tof.my_object_number
                self.laserData.append(data)
        self.mutex.release()
        return True

    def getLaserData(self):
        self.mutex.acquire()
        ret = self.laserData
        self.mutex.release()
        return ret

    def getLaserConfData(self):
        ret = LaserConfData()
        return ret

    def getLaserAndBStateData(self):
        ret = TLaserData()
        bState = RoboCompGenericBase.TBaseState()
        return [ret, bState]
