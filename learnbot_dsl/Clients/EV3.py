from learnbot_dsl.Clients.Client import *
from learnbot_dsl.Clients.Devices import *
from learnbot_dsl.functions import getFuntions
import math, traceback, sys, tempfile, os
from threading import Event
import rpyc

K = 30
L = 120
MAXSPEED = 1000

class Robot(Client):

    devicesAvailables = ["base"]

    def __init__(self):
        self.ev3 = None
        self.motorR = None
        self.motorL = None
        self.connectToRobot()
        self.base = Base(_callFunction=self.deviceBaseMove)
        self.motorSpeed = [0, 0]
        self.currentMotorSpeed = [-1, -1]
        Client.__init__(self, _miliseconds=100)
        self.start()

    def connectToRobot(self):
        self. conn = rpyc.classic.connect('192.168.0.119')  # host name or IP address of the EV3
        self.ev3 = self.conn.modules['ev3dev.ev3']  # import ev3dev.ev3 remotely
        self.motorR = self.ev3.LargeMotor('outD')
        self.motorL = self.ev3.LargeMotor('outB')


    def disconnect(self):
        self.motorR.run_timed(time_sp=100, speed_sp=0)
        self.motorL.run_timed(time_sp=100, speed_sp=0)


    def deviceBaseMove(self, SAdv, SRot):
        if SRot != 0.:
            Rrot = SAdv / math.tan(SRot)

            Rl = Rrot - (L / 2)
            r_wheel_speed = SRot * Rl * 360/ (2 * math.pi * K)

            Rr = Rrot + (L / 2)
            l_wheel_speed = SRot * Rr * 360/ (2 * math.pi * K)
        else:
            l_wheel_speed = SAdv * 360/ (2 * math.pi * K)
            r_wheel_speed = SAdv * 360/ (2 * math.pi * K)
        print("rspeed", r_wheel_speed, "lspeed", l_wheel_speed)
        self.motorR.run_forever(speed_sp = int(r_wheel_speed))
        self.motorL.run_forever(speed_sp = int(l_wheel_speed))


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
