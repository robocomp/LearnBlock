#!/usr/bin/env python
# -*- coding: utf-8 -*-
from learnbot_dsl.Client import *
import os, Ice, numpy as np, PIL.Image as Image, io, cv2, paho.mqtt.client

ROBOCOMP = ''
try:
    ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
    print('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
    ROBOCOMP = os.path.join('opt', 'robocomp')

ICEs = ["Laser.ice", "DifferentialRobot.ice", "JointMotor.ice", "EmotionalMotor.ice", "GenericBase.ice"]

icePaths = [os.path.join(os.path.dirname(__file__), "interfaces")]
for ice in ICEs:
    for p in icePaths:
        if os.path.isfile(os.path.join(p, ice)):
            wholeStr = ' -I' + p + " --all " + os.path.join(p, ice)
            Ice.loadSlice(wholeStr)
            break

import RoboCompLaser, RoboCompDifferentialRobot, RoboCompJointMotor, RoboCompGenericBase, RoboCompEmotionalMotor

open_cv_image = np.zeros((240,320,3), np.uint8)
newImage = False
def on_message(client, userdata, message):
    global open_cv_image, newImage
    newImage = True
    data = message.payload
    image_stream = io.BytesIO()
    image_stream.write(data)
    image = Image.open(image_stream)
    open_cv_image = np.array(image)
    open_cv_image = cv2.flip(open_cv_image, 0)

laser_proxy = connectComponent("laser:tcp -h 192.168.16.1 -p 10104", RoboCompLaser.LaserPrx)
differentialrobot_proxy = connectComponent("differentialrobot:tcp -h 192.168.16.1 -p 10004", RoboCompDifferentialRobot.DifferentialRobotPrx)

def readLaser():
    global laser_proxy
    laserdata = laser_proxy.getLaserData()
    usList = [d.dist for d in laserdata]
    return {"front": usList[1:4],  # The values must be in mm
            "left": usList[:2],
            "right": usList[3:]}

def move(_adv, _rot):
    global differentialrobot_proxy
    differentialrobot_proxy.setSpeedBase(-_adv * 8, _rot * 15)

def readCamera():
    return open_cv_image, newImage

class Robot(Client):

    def __init__(self):
        Client.__init__(self)
        self.emotionalmotor_proxy = connectComponent("emotionalmotor:tcp -h 192.168.16.1 -p 30001", RoboCompEmotionalMotor.EmotionalMotorPrx)
        self.jointmotor_proxy = connectComponent("jointmotor:tcp -h 192.168.16.1 -p 10067", RoboCompJointMotor.JointMotorPrx)
        try:
            # self.client = paho.mqtt.client.Client(client_id='learnbotClient', clean_session=False)
            self.client = paho.mqtt.client.Client()
            self.client.on_message = on_message
            self.client.connect(host='192.168.16.1', port=50000)
            self.client.subscribe(topic='camara', qos=2)
            self.client.loop_start()
            print("Streamer iniciado correctamente")
        except Exception as e:
            print("Error connect Streamer\n", e)

        self.distanceSensors = DistanceSensors(_readFunction=readLaser)
        # self.acelerometer = Acelerometer(_readFunction=)
        # self.gyroscope = Gyroscope(_readFunction=)
        self.camera = Camera(_readFunction=readCamera)
        self.base = Base(_callFunction=move,_max_rot=0.4)

    def expressJoy(self):
        try:
            self.emotionalmotor_proxy.expressJoy()
            self.currentEmotion = Emotions.Joy
        except Exception as e:
            print("Error expressJoy\n",e)

    def expressSadness(self):
        try:
            self.emotionalmotor_proxy.expressSadness()
            self.currentEmotion = Emotions.Sadness
        except Exception as e:
            print("Error expressSadness\n",e)

    def expressSurprise(self):
        try:
            self.emotionalmotor_proxy.expressSurprise()
            self.currentEmotion = Emotions.Surprise
        except Exception as e:
            print("Error expressSurprise\n",e)

    def expressFear(self):
        try:
            self.emotionalmotor_proxy.expressFear()
            self.currentEmotion = Emotions.Fear
        except Exception as e:
            print("Error expressFear\n",e)

    def expressAnger(self):
        try:
            self.emotionalmotor_proxy.expressAnger()
            self.currentEmotion = Emotions.Anger
        except Exception as e:
            print("Error expressAnger\n",e)

    def expressDisgust(self):
        try:
            self.emotionalmotor_proxy.expressDisgust()
            self.currentEmotion = Emotions.Disgust
        except Exception as e:
            print("Error expressDisgust\n",e)

    def expressNeutral(self):
        try:
            self.emotionalmotor_proxy.expressNeutral()
            self.currentEmotion = Emotions.Neutral
        except Exception as e:
            print("Error expressNeutral\n",e)

    def setJointAngle(self, angle):
        self.angleCamera = angle
        goal = RoboCompJointMotor.MotorGoalPosition()
        goal.name = 'servo'
        goal.position = angle
        self.jointmotor_proxy.setPosition(goal)

if __name__ == '__main__':

    ebo = Robot()
    ebo.start()
    ebo.setRobotSpeed(0,0)