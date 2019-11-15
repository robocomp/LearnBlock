#!/usr/bin/env python
# -*- coding: utf-8 -*-
from learnbot_dsl.Clients.Client import *
from learnbot_dsl.functions import getFuntions
import os, numpy as np, PIL.Image as Image, PIL.ImageFilter as ImageFilter, io, cv2, paho.mqtt.client, threading, math
import cozmo as cozmoR
from cozmo.util import radians, degrees, distance_mm, speed_mmps
from learnbot_dsl.Clients.Devices import *

cozmo = None
K = 1  # Speed constant
L = 45  # Distance between wheels


def cozmo_program(_robot: cozmoR.robot.Robot):
    global cozmo
    global stopThread
    cozmo = _robot
    while not stopThread:
        pass

class Robot(Client):

    def __init__(self):
        global cozmo
        global stopThread
        stopThread = False
        Client.__init__(self)
        self.addGroundSensors(GroundSensors(_readFunction=self.deviceReadGSensor))
        self.addAcelerometer(Acelerometer(_readFunction=self.deviceReadAcelerometer))
        self.addGyroscope(Gyroscope(_readFunction=self.deviceReadGyroscope, _resetFunction=self.deviceResetGyroscope), "Z_AXIS")
        self.addCamera(Camera(_readFunction=self.deviceReadCamera))
        self.addBase(Base(_callFunction=self.deviceMove))
        self.addDisplay(Display(_setEmotion=self.deviceSendEmotion, _setImage=None))
        self.addJointMotor(JointMotor(_callDevice=self.deviceSendAngleHead, _readDevice=None), "CAMERA")
        self.addJointMotor(JointMotor(_callDevice=self.deviceSendAngleArm, _readDevice=None), "ARM")
        self.addSpeaker(Speaker(_sendText=self.deviceSendText))
        self.connectToRobot()
        self.cozmo = cozmo
        self.cozmo.camera.image_stream_enabled = True
        self.cozmo.camera.color_image_enabled = True
        self.cozmo.enable_device_imu(enable_raw=True, enable_gyro = True)
        self.current_pose_angle = 0
        self.vueltas = 0
        self.last_pose_read = 0
        self.start()

    def connectToRobot(self):
        cozmoR.robot.Robot.drive_off_charger_on_connect = False
        self.t = threading.Thread(target=lambda: cozmoR.run_program(cozmo_program))
        self.t.start()
        time.sleep(2)

    def disconnect(self):
        print("disconnecting")
        self.deviceMove(0,0)
        self.cozmo.wait_for_all_actions_completed()
        global stopThread
        stopThread = True

    def deviceSendText(self, text):
        self.cozmo.say_text(text=text, in_parallel=True)

    def deviceSendAngleArm(self, _angle):
        angle_rad = math.radians(_angle)
        if angle_rad > 0.79:
            angle_rad = 0.79
        elif angle_rad < -0.20:
            angle_rad = -0.20
        a = (angle_rad + 0.20) / (0.79 + 0.20)
        self.cozmo.set_lift_height(a, in_parallel=True)

    def deviceSendAngleHead(self, _angle):
        a = degrees(_angle)
        self.cozmo.set_head_angle(a, in_parallel=True)

    def deviceSendEmotion(self, _emotion):
        if self.cozmo.has_in_progress_actions:
            return
        trigger = None
        if _emotion is Emotions.Joy:
            trigger = cozmoR.anim.Triggers.PeekABooGetOutHappy
        elif _emotion is Emotions.Sadness:
            trigger = cozmoR.anim.Triggers.PeekABooGetOutSad
        elif _emotion is Emotions.Surprise:
            trigger = cozmoR.anim.Triggers.PeekABooSurprised
        elif _emotion is Emotions.Disgust:
            trigger = None
        elif _emotion is Emotions.Anger:
            trigger = cozmoR.anim.Triggers.DriveEndAngry
        elif _emotion is Emotions.Fear:
            trigger = cozmoR.anim.Triggers.CodeLabScaredCozmo
        elif _emotion is Emotions.Neutral:
            trigger = cozmoR.anim.Triggers.NeutralFace
        if trigger is not None:
            self.cozmo.play_anim_trigger(trigger, in_parallel=True, ignore_body_track=True,
                                         ignore_head_track=True, ignore_lift_track=True)

    def deviceReadGyroscope(self):
        rz_n = self.cozmo.pose.rotation.angle_z.degrees
        if rz_n < 0:
            rz_n = 360 + rz_n
        if math.fabs(self.last_pose_read-rz_n) > 180:
            self.vueltas = self.vueltas+np.sign(self.last_pose_read-rz_n)
        self.last_pose_read = rz_n
        rz = rz_n - self.current_pose_angle + self.vueltas*360
        print("Cozmo gyro", rz_n, rz)
        return int(-rz)

    def deviceResetGyroscope(self):
        self.vueltas=0
        self.current_pose_angle = self.cozmo.pose.rotation.angle_z.degrees
        if self.current_pose_angle < 0:
            self.current_pose_angle = 360 + self.current_pose_angle
        self.last_pose_read = self.current_pose_angle

    def deviceReadAcelerometer(self):
        return self.cozmo.accelerometer.x_y_z

    def deviceReadGSensor(self):
        if self.cozmo.is_cliff_detected:
            ground = 0
        else:
            ground = 100
        return {"central": ground}

    def deviceReadCamera(self):
        lastimg = self.cozmo.world.latest_image
        if lastimg is not None:
            img = lastimg.annotate_image()
            open_cv_image = np.array(img.convert('RGB'))
            cv_image = open_cv_image[:, :, ::-1].copy()
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
            return cv_image, True
        else:
            print("error leyendo camara")
            return None, False

    def deviceMove(self, SAdv, SRot):
        SRot_rad = math.radians(SRot)
        if SRot_rad != 0.:
            Rrot = SAdv / SRot_rad

            Rl = Rrot - (L / 2)
            l_wheel_speed = SRot_rad * Rl * 2

            Rr = Rrot + (L / 2)
            r_wheel_speed = SRot_rad * Rr * 2
        else:
            l_wheel_speed = SAdv * K
            r_wheel_speed = SAdv * K
        self.cozmo.drive_wheel_motors(r_wheel_speed, l_wheel_speed, 0, 0)


if __name__ == '__main__':
    robot = Robot()
    robot.speakText("hola")
    robot.join()
