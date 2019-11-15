#!/usr/bin/env python
# -*- coding: utf-8 -*-
from learnbot_dsl.Clients.Client import *
from learnbot_dsl.Clients.Devices import *
import os, Ice, numpy as np, io, cv2, threading, json, math
import learnbot_dsl.Clients.Devices as Devices
from PIL import Image, ImageDraw
from random import randint
from learnbot_dsl import path as Learnblock_Path
from learnbot_dsl import PATHINTERFACES



ROBOCOMP = ''
try:
    ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
    print('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
    ROBOCOMP = os.path.join('opt', 'robocomp')

ICEs = ["Laser.ice", "DifferentialRobot.ice", "JointMotor.ice", "EmotionalMotor.ice", "RGBD.ice", "GenericBase.ice"]
icePaths = []
icePaths.append(PATHINTERFACES)
for ice in ICEs:
    for p in icePaths:
        if os.path.isfile(os.path.join(p, ice)):
            wholeStr = ' -I' + p + " --all " + os.path.join(p, ice)
            Ice.loadSlice(wholeStr)
            break

import RoboCompLaser, RoboCompDifferentialRobot, RoboCompJointMotor, RoboCompGenericBase, RoboCompEmotionalMotor, RoboCompRGBD


class Robot(Client):

    def __init__(self):
        self.connectToRobot()
        Client.__init__(self)

        self.open_cv_image = np.zeros((240, 320, 3), np.uint8)
        self.newImage = False
        self.addDistanceSensors(Devices.DistanceSensors(_readFunction=self.deviceReadLaser))
        self.addCamera(Devices.Camera(_readFunction=self.deviceReadCamera))
        self.addBase(Devices.Base(_callFunction=self.deviceMove))
        self.addDisplay(Devices.Display(_setEmotion=self.deviceSendEmotion, _setImage=None))
        self.addJointMotor(Devices.JointMotor(_callDevice=self.deviceSendAngleHead, _readDevice=None), "CAMERA")
        self.start()

    def connectToRobot(self):
        configRobot = {}
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "EBO_remote_sim.cfg"), "rb") as f:
            configRobot = json.loads(f.read())
        self.laser_proxys = []
        # Remote object connection for Lasers
        robotIP = configRobot["RobotIP"]
        self.differentialrobot_proxy = connectComponent("differentialrobot:tcp -h " + robotIP + " -p 10004",
                                                        RoboCompDifferentialRobot.DifferentialRobotPrx)
        self.deviceMove(0,0)

        for i in range(2, 7):
            self.laser_proxys.append(connectComponent("laser:tcp -h " + robotIP + " -p 1010" + str(i), RoboCompLaser.LaserPrx))

        self.jointmotor_proxy = connectComponent("jointmotor:tcp -h " + robotIP + " -p 20000",
                                                 RoboCompJointMotor.JointMotorPrx)

        self.emotionalmotor_proxy = connectComponent("emotionalmotor:tcp -h " + robotIP + " -p 30001",
                                                     RoboCompEmotionalMotor.EmotionalMotorPrx)

        self.rgbd_proxy = connectComponent("rgbd:tcp -h " + robotIP + " -p 10097", RoboCompRGBD.RGBDPrx)

    def disconnect(self):
        self.deviceMove(0, 0)

    def deviceReadLaser(self):
        usList = []
        for prx in self.laser_proxys:
            laserdata = prx.getLaserData()
            usList.append(min([x.dist for x in laserdata]))
        #print(usList)
        return {"front": usList[1:4],  # The values must be in mm
                "left": usList[:2],
                "right": usList[3:]}

    def deviceMove(self, _adv, _rot):
        self.differentialrobot_proxy.setSpeedBase(_adv, math.radians(_rot))

    def deviceReadCamera(self, ):
        color, depth, headState, baseState = self.rgbd_proxy.getData()
        if (len(color) == 0) or (len(depth) == 0):
            print('Error retrieving images!')
        image = np.fromstring(color, dtype=np.uint8).reshape((240, 320, 3))
        return image, True

    def deviceSendEmotion(self, _emotion):
        if _emotion is Emotions.Joy:
            self.emotionalmotor_proxy.expressJoy()
        elif _emotion is Emotions.Sadness:
            self.emotionalmotor_proxy.expressSadness()
        elif _emotion is Emotions.Surprise:
            self.emotionalmotor_proxy.expressSurprise()
        elif _emotion is Emotions.Disgust:
            self.emotionalmotor_proxy.expressDisgust()
        elif _emotion is Emotions.Anger:
            self.emotionalmotor_proxy.expressAnger()
        elif _emotion is Emotions.Fear:
            self.emotionalmotor_proxy.expressFear()
        elif _emotion is Emotions.Neutral:
            self.emotionalmotor_proxy.expressNeutral()

    def deviceSendAngleHead(self, _angle):
        goal = RoboCompJointMotor.MotorGoalPosition()
        goal.name = 'servo'
        goal.position = -math.radians(_angle)
        self.jointmotor_proxy.setPosition(goal)


if __name__ == '__main__':
    ebo = Robot()
    ebo.start()
    ebo.setBaseSpeed(0, 0)
    ebo.setJointAngle("CAMERA", 30)
