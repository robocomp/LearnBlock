from learnbot_dsl.Clients.Client import *
from learnbot_dsl.Clients.Devices import *
from learnbot_dsl.functions import getFuntions
import math, traceback, sys, tempfile, os
from threading import Event
import rpyc, time

K = 30
L = 120
MAXSPEED = 1000

class Robot(Client):

    def __init__(self):
        Client.__init__(self, _miliseconds=100)
        self.ev3Motor = None
        self.ev3Sensors = None
        self.ev3Base = None
        self.connectToRobot()
        self.addBase(Base(_callFunction=self.deviceBaseMove))
        self.addDistanceSensors(DistanceSensors(_readFunction=self.deviceReadSonar))
        self.addGroundSensors(GroundSensors(_readFunction=self.deviceReadGroundSensors))
        self.addGyroscope(Gyroscope(_readFunction=self.deviceReadGyroscope, _resetFunction=self.deviceResetGyroscope), "Z_AXIS")
        self.start()

    def connectToRobot(self):
        configRobot = {}
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "EV3.cfg"), "rb") as f:
            configRobot = json.loads(f.read())
        robotIP = configRobot["RobotIP"]
        self. conn = rpyc.classic.connect(robotIP)  # host name or IP address of the EV3
        self.ev3Motor = self.conn.modules['ev3dev2.motor']  # import ev3dev.ev3 remotely
        LEFT_MOTOR = self.ev3Motor.OUTPUT_B
        RIGHT_MOTOR = self.ev3Motor.OUTPUT_D
        self.ev3Base = self.ev3Motor.MoveTank(LEFT_MOTOR, RIGHT_MOTOR)
        self.ev3Sensors = self.conn.modules['ev3dev2.sensor.lego']
        self.ultrasonic = self.ev3Sensors.UltrasonicSensor()
        self.colorsensor = self.ev3Sensors.ColorSensor() 
        self.colorsensor.mode = 'COL-REFLECT'
        self.gyrosensor = self.ev3Sensors.GyroSensor()
        self.gyrosensor.mode = 'GYRO-ANG'


    def disconnect(self):
        self.ev3Base.stop()

    def deviceBaseMove(self, SAdv, SRot):
        SRot_rad = math.radians(SRot)        
        if SRot != 0.:
            #Rrot = SAdv / math.tan(SRot_rad)
            Rrot = SAdv / SRot_rad

            Rl = Rrot - (L / 2)
            r_wheel_speed = SRot_rad * Rl * 360/ (2 * math.pi * K)

            Rr = Rrot + (L / 2)
            l_wheel_speed = SRot_rad * Rr * 360/ (2 * math.pi * K)
        else:
            l_wheel_speed = SAdv * 360/ (2 * math.pi * K)
            r_wheel_speed = SAdv * 360/ (2 * math.pi * K)
        #print("rspeed", r_wheel_speed, "lspeed", l_wheel_speed)
        self.ev3Base.on(left_speed=self.ev3Motor.SpeedDPS(l_wheel_speed), right_speed=self.ev3Motor.SpeedDPS(r_wheel_speed))

    def deviceReadSonar(self):
        dist = self.ultrasonic.value()
        return {"front": [dist],  # The values must be in mm
                "left": [2000],
                "right": [2000],
                "back": [2000]}

    def deviceReadGroundSensors(self):
        ground = self.colorsensor.value()
        return {"central": ground}

    def deviceReadGyroscope(self):
        rz = self.gyrosensor.value()
        return rz

    def deviceResetGyroscope(self):
        self.gyrosensor.mode = 'GYRO-CAL'
        self.gyrosensor.mode = 'GYRO-ANG'



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


