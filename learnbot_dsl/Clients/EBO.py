#!/usr/bin/env python
# -*- coding: utf-8 -*-
from learnbot_dsl.Clients.Client import *
from learnbot_dsl.Clients.Devices import *
import os, Ice, numpy as np, PIL.Image as Image, io, cv2, paho.mqtt.client
import learnbot_dsl.Clients.Devices as Devices
from learnbot_dsl.functions import getFuntions

ROBOCOMP = ''
try:
    ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
    print('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
    ROBOCOMP = os.path.join('opt', 'robocomp')

ICEs = ["Laser.ice", "DifferentialRobot.ice", "JointMotor.ice", "EmotionalMotor.ice", "GenericBase.ice"]
icePaths = []
icePaths.append("/home/ivan/robocomp/components/learnbot/learnbot_dsl/interfaces")
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
    # open_cv_image = cv2.flip(open_cv_image, 0)

laser_proxy = connectComponent("laser:tcp -h 192.168.16.1 -p 10104", RoboCompLaser.LaserPrx)
differentialrobot_proxy = connectComponent("differentialrobot:tcp -h 192.168.16.1 -p 10004", RoboCompDifferentialRobot.DifferentialRobotPrx)
jointmotor_proxy = connectComponent("jointmotor:tcp -h 192.168.16.1 -p 10067", RoboCompJointMotor.JointMotorPrx)
emotionalmotor_proxy = connectComponent("emotionalmotor:tcp -h 192.168.16.1 -p 30001",
                                             RoboCompEmotionalMotor.EmotionalMotorPrx)


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

def sendEmotion(_emotion):
    if Emotions.Joy:
        emotionalmotor_proxy.expressJoy()
    elif Emotions.Sadness:
        emotionalmotor_proxy.expressSadness()
    elif Emotions.Surprise:
        emotionalmotor_proxy.expressSurprise()
    elif Emotions.Disgust:
        emotionalmotor_proxy.expressDisgust()
    elif Emotions.Anger:
        emotionalmotor_proxy.expressAnger()
    elif Emotions.Fear:
        emotionalmotor_proxy.expressFear()
    elif Emotions.Neutral:
        emotionalmotor_proxy.expressNeutral()

def sendAngleHead(_angle):
    goal = RoboCompJointMotor.MotorGoalPosition()
    goal.name = 'servo'
    goal.position = _angle
    jointmotor_proxy.setPosition(goal)

addFunctions(getFuntions())

class Robot(Client):

    def __init__(self):
        Client.__init__(self)
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

        self.distanceSensors = Devices.DistanceSensors(_readFunction=readLaser)
        self.camera = Devices.Camera(_readFunction=readCamera)
        self.base = Devices.Base(_callFunction=move)
        self.display = Devices.Display(_setEmotion=sendEmotion, _setImage=None)
        self.addJointMotor("CAMERA", _JointMotor=Devices.JointMotor(_callDevice= sendAngleHead, _readDevice=None))
        self.start()


if __name__ == '__main__':
    ebo = Robot()
    ebo.start()
    ebo.setBaseSpeed(0,0)
    ebo.setJointAngle("CAMERA", 0.6000000238)