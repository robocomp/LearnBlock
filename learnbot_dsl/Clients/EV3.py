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

    devicesAvailables = ["base","distancesensors", "groundsensors", "gyroscope"]

    def __init__(self):
        self.ev3Motor = None
        self.ev3Sensors = None
        self.ev3Base = None
        self.connectToRobot()
        self.base = Base(_callFunction=self.deviceBaseMove)
	self.addJointMotor("ARM", _JointMotor=JointMotor(_callDevice=self.deviceSendAngleArm, _readDevice=None))
        self.distanceSensors = DistanceSensors(_readFunction=self.deviceReadLaser)
        self.groundSensors = GroundSensors(_readFunction=self.deviceReadGroundSensors)
        self.gyroscope = Gyroscope(_readFunction=self.deviceReadGyroscope, _resetFunction=self.resetGyroscope)
        self.motorSpeed = [0, 0]
        self.currentMotorSpeed = [-1, -1]
        Client.__init__(self, _miliseconds=100)
        self.start()

    def connectToRobot(self):
        self. conn = rpyc.classic.connect('192.168.0.113')  # host name or IP address of the EV3
        self.ev3Motor = self.conn.modules['ev3dev2.motor']  # import ev3dev.ev3 remotely
        LEFT_MOTOR = self.ev3Motor.OUTPUT_B
        RIGHT_MOTOR = self.ev3Motor.OUTPUT_D
        self.ev3Base = self.ev3Motor.MoveTank(LEFT_MOTOR, RIGHT_MOTOR)
	ARM_MOTOR = self.ev3Motor.OUTPUT_A
	self.ev3Arm = self.ev3Motor.ServoMotor(ARM_MOTOR)
        self.ev3Sensors = self.conn.modules['ev3dev2.sensor.lego']
        self.ultrasonic = self.ev3Sensors.UltrasonicSensor()
        self.colorsensor = self.ev3Sensors.ColorSensor() 
        self.colorsensor.mode = 'COL-REFLECT'
        self.gyrosensor = self.ev3Sensors.GyroSensor()
        self.gyrosensor.mode = 'GYRO-ANG'


    def disconnect(self):
        self.ev3Base.on(left_speed=0, right_speed=0)

    def deviceBaseMove(self, SAdv, SRot):
        if SRot != 0.:
            #Rrot = SAdv / math.tan(SRot)
            Rrot = SAdv / SRot

            Rl = Rrot - (L / 2)
            r_wheel_speed = SRot * Rl * 360/ (2 * math.pi * K)

            Rr = Rrot + (L / 2)
            l_wheel_speed = SRot * Rr * 360/ (2 * math.pi * K)
        else:
            l_wheel_speed = SAdv * 360/ (2 * math.pi * K)
            r_wheel_speed = SAdv * 360/ (2 * math.pi * K)
        #print("rspeed", r_wheel_speed, "lspeed", l_wheel_speed)
        self.ev3Base.on(left_speed=self.ev3Motor.SpeedDPS(l_wheel_speed), right_speed=self.ev3Motor.SpeedDPS(r_wheel_speed))

    def deviceSendAngleArm(self, _angle):
        if _angle > 100 :
            _angle = 100
        elif _angle < -100:
            _angle = -100
	#calculamos valor del angulo a enviar	
	if _angle = 0:
	    a = mid_pulse_sp
	elif _angle = -100:
	    a = min_pulse_sp
	elif _angle = 100:
	    a = max_pulse_sp
	elif _angle < 0 and _angle > -100:
	    a = - ( 
            #a = (_angle + 100) / (100 + (-100))

	self.ev3Arm.position_sp = a
	self.ev3Arm.run()		#move the servo to the value of position_sp()

    def deviceReadLaser(self):
        dist = self.ultrasonic.value()
        return {"front": [dist],  # The values must be in mm
                "left": [2000],
                "right": [2000],
                "back": [2000]}

    def deviceReadGroundSensors(self):
        ground = self.colorsensor.value()
        return {"left": ground,
                "right": ground}

    def deviceReadGyroscope(self):
        ry = self.gyrosensor.value()
        return 0, ry, 0

    def resetGyroscope(self):
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
