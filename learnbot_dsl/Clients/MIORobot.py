from learnbot_dsl.Clients.Client import *
from learnbot_dsl.Clients.Devices import *
from learnbot_dsl.functions import getFuntions
import math, traceback, sys, tempfile, os
from threading import Event
import rpyc, time

from learnbot_dsl.Clients.Third_Party.MIOLib import lib #

K = 30
L = 120
MAXSPEED = 1000

class Robot(Client):

    def __init__(self):
        Client.__init__(self, _miliseconds=100)
        self.connectToRobot()
        self.addBase(Base(_callFunction=self.deviceBaseMove))
        self.start()

    def connectToRobot(self):
        pass

    def disconnect(self):
        pass #parar la base

    def deviceBaseMove(self, SAdv, SRot):
        pass



if __name__ == '__main__':
    try:
        robot = Robot()
    except Exception as e:
        print("hay un Error")
        traceback.print_exc()
        raise (e)
    print(dir(robot))
    time_global_start = time.time()

    robot.stop_bot()


    def elapsedTime(umbral):
        global time_global_start
        time_global = time.time() - time_global_start
        return time_global > umbral


