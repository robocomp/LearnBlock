from learnbot_dsl.Clients.Client import *
from learnbot_dsl.Clients.Devices import *
from learnbot_dsl.functions import getFuntions
import math, traceback, sys, tempfile, os
from threading import Event
import rpyc

K = 30
L = 120

class Robot(Client):

    devicesAvailables = ["base"]

    def __init__(self):
        self.connectToRobot()
        self.deviceBaseMove(0,0)
        self.base = Base(_callFunction=self.deviceBaseMove)
        self.motorSpeed = [0, 0]
        self.currentMotorSpeed = [-1, -1]
        Client.__init__(self, _miliseconds=100)
        self.start()

    def connectToRobot(self):
        conn = rpyc.classic.connect('192.168.0.119')  # host name or IP address of the EV3
        self.ev3 = conn.modules['ev3dev.ev3']  # import ev3dev.ev3 remotely
        self.motorR = self.ev3.LargeMotor('outD')
        self.motorL = self.ev3.LargeMotor('outB')


    def disconnect(self):
        self.deviceBaseMove(0, 0)

    def deviceBaseMove(self, SAdv, SRot):
        if SRot != 0.:
            Rrot = SAdv / math.tan(SRot)

            Rl = Rrot - (L / 2)
            r_wheel_speed = SRot * Rl / K

            Rr = Rrot + (L / 2)
            l_wheel_speed = SRot * Rr / K
        else:
            l_wheel_speed = SAdv / K
            r_wheel_speed = SAdv / K
        self.motorR.run_forever(speed_sp = r_wheel_speed)
        self.motorL.run_forever(speed_sp = l_wheel_speed)



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

    # try:
    #     while True:
    #
    #         if robot.front_obstacle(50):
    #             robot.stop_bot()
    #         else:
    #             robot.move_straight()
    #         print("bucle")
    # finally:
    #     print("quit")
