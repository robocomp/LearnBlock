#!/usr/bin/env python
# -*- coding: utf-8 -*-
from learnbot_dsl.Clients.Client import *
from learnbot_dsl.functions import getFuntions
import os, numpy as np, PIL.Image as Image, PIL.ImageFilter as ImageFilter, io, cv2, paho.mqtt.client, threading, math
import cozmo
from cozmo.util import radians, degrees, distance_mm, speed_mmps
from learnbot_dsl.Clients.Devices import *

cozmo = None
K = 2                      # Speed constant
L = 45                       # Distance between wheels

def cozmo_program(_robot: cozmo.robot.Robot):
    global cozmo
    cozmo = _robot
    while True:
        pass


class Robot(Client):
    requiementFunctions = ['is_there_blue_line', 'center_face', 'left_black_line', 'am_I_moving_right', 'left_blue_line', 'is_there_face', 'is_there_somebody_happy', 'move_right', 'expressNeutral', 'am_I_Surprise', 'up_face', 'sleep', 'turn_90_right', 'am_I_Sadness', 'am_I_Joy', 'is_there_black_line', 'expressJoy', 'obstacle_free', 'is_there_red_line', 'near_to_target', 'am_I_Angry', 'back_obstacle', 'right_black_line', 'am_I_moving_left', 'is_there_somebody_angry', 'move_left', 'look_floor', 'look_front', 'front_obstacle', 'right_blue_line', 'am_I_turning_right', 'turn_left', 'turn_right', 'target_at_left', 'expressSurprise', 'center_red_line', 'look_up', 'target_at_front', 'am_I_moving_straight', 'get_distance', 'turn_back', 'am_I_turning', 'center_black_line', 'left_face', 'set_move', 'setAngleCamera', 'line_crossing', 'right_red_line', 'down_camera', 'slow_down', 'is_there_somebody_neutral', 'seeing_the_tag', 'expressDisgust', 'setAngleMotor', 'right_face', 'target_at_right', 'stop_bot', 'get_image', 'expressAnger', 'center_blue_line', 'expressFear', 'get_pose', 'sayText', 'move_straight', 'am_I_Disgust', 'am_I_Neutral', 'expressSadness', 'turn', 'is_there_somebody_surprised', 'left_obstacle', 'is_there_somebody_sad', 'turn_90_left', 'down_face', 'am_I_Scared', 'up_camera', 'right_obstacle', 'left_red_line', 'am_I_turning_left']

    def __init__(self):
        global cozmo
        Client.__init__(self)
        self.distanceSensors = DistanceSensors(_readFunction=self.deviceReadLaser)
        self.acelerometer = Acelerometer(_readFunction=self.deviceReadAcelerometer)
        self.gyroscope = Gyroscope(_readFunction=self.deviceReadGyroscope)
        self.camera = Camera(_readFunction=self.deviceReadCamera)
        self.base = Base(_callFunction=self.deviceMove)
        self.display = Display(_setEmotion=self.deviceSendEmotion, _setImage=None)
        self.addJointMotor("CAMERA", _JointMotor=JointMotor(_callDevice= self.deviceSendAngleHead, _readDevice=None))
        self.addJointMotor("ARM", _JointMotor=JointMotor(_callDevice= self.deviceSendAngleArm, _readDevice=None))
        self.speaker = Speaker(_sendText=self.deviceSendText)
        self.connectToRobot()
        self.cozmo = cozmo
        self.start()

    def connectToRobot(self):
        cozmo.robot.Robot.drive_off_charger_on_connect = False
        self.t = threading.Thread(target=lambda: self.cozmo.run_program(cozmo_program)).start()
        time.sleep(2)
        self.cozmo.camera.image_stream_enabled = True
        self.cozmo.camera.color_image_enabled = True

    def deviceSendText(self,text):
        self.cozmo.say_text(text=text, in_parallel=True)

    def deviceSendAngleArm(self, _angle):
        if _angle > 0.79:
            _angle = 0.79
        elif _angle < -0.20:
            _angle = -0.20
        a = (_angle + 0.20) / (0.79 + 0.20)
        self.cozmo.set_lift_height(a, in_parallel=True)

    def deviceSendAngleHead(self, _angle):
        a = radians(_angle)
        self.cozmo.set_head_angle(a, in_parallel=True)

    def deviceSendEmotion(self, _emotion):
        if self.cozmo.has_in_progress_actions:
            return
        trigger = None
        if _emotion is Emotions.Joy:
            trigger = cozmo.anim.Triggers.PeekABooGetOutHappy
        elif _emotion is Emotions.Sadness:
            trigger = cozmo.anim.Triggers.PeekABooGetOutSad
        elif _emotion is Emotions.Surprise:
            trigger = cozmo.anim.Triggers.PeekABooSurprised
        elif _emotion is Emotions.Disgust:
            trigger = None
        elif _emotion is Emotions.Anger:
            trigger = cozmo.anim.Triggers.DriveEndAngry
        elif _emotion is Emotions.Fear:
            trigger = cozmo.anim.Triggers.CodeLabScaredCozmo
        elif _emotion is Emotions.Neutral:
            trigger = cozmo.anim.Triggers.NeutralFace
        if trigger is not None:
            self.cozmo.play_anim_trigger(trigger, in_parallel=True, ignore_body_track=True,
                                     ignore_head_track=True, ignore_lift_track=True)

    def deviceReadGyroscope(self):
        return self.cozmo.gyro.x_y_z

    def deviceReadAcelerometer(self):
        return self.cozmo.accelerometer.x_y_z

    def deviceReadLaser(self):
        return {"bottom": [self.cozmo.is_cliff_detected]}

    def deviceReadCamera(self):
        img = self.cozmo.world.latest_image.annotate_image()
        open_cv_image = np.array(img.convert('RGB'))
        cv_image = open_cv_image[:, :, ::-1].copy()
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        return cv_image, True

    def deviceMove(self, SAdv, SRot):
        if SRot != 0.:
            print(SRot)
            Rrot = SAdv / math.tan(SRot)

            Rl = Rrot - (L / 2)
            l_wheel_speed = SRot * Rl * K

            Rr = Rrot + (L / 2)
            r_wheel_speed = SRot * Rr * K
        else:
            l_wheel_speed = SAdv * K
            r_wheel_speed = SAdv * K
        self.cozmo.drive_wheel_motors(r_wheel_speed, l_wheel_speed, 0, 0)

if __name__ == '__main__':
    ebo = Robot()
    ebo.speakText("hola")
    ebo.join()
