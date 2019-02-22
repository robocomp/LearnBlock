#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
from threading import Thread, Lock, Event
import numpy as np, copy, sys, time, Ice, os, subprocess
from learnbot_dsl.Clients.Devices import *

__ICEs = ["EmotionRecognition.ice", "Apriltag.ice" ]
__icePaths = []
__icePaths.append("/home/ivan/robocomp/components/learnbot/learnbot_dsl/interfaces")
for ice in __ICEs:
    for p in __icePaths:
        if os.path.isfile(os.path.join(p, ice)):
            wholeStr = ' -I' + p + " --all " + os.path.join(p, ice)
            Ice.loadSlice(wholeStr)
            break

import RoboCompEmotionRecognition
import RoboCompApriltag



def connectComponent(stringProxy, _class):
    ic = Ice.initialize(sys.argv)
    i = 0
    while (True):
        try:
            i += 1
            basePrx = ic.stringToProxy(stringProxy)
            proxy = _class.checkedCast(basePrx)
            print("Connection Successful: ", stringProxy)
            break
        except Ice.Exception as e:
            if i is 4:
                print("Cannot connect to the proxy: ", stringProxy)
                return None
            else:
                time.sleep(1.5)
    return proxy

class Client(Thread):
    __cameraMoveAvailable = False
    __angleCamera = 0                               # The values must be in rad

    # Variables of Emotion Recognition
    __emotion_current_exist = False
    __currents_emotions = []
    __currentEmotion = Emotions.NoneEmotion

    # Variables of AprilTag
    __apriltag_current_exist = False
    __listAprilIDs = []

    __stop_event = Event()
    active = False

    acelerometer = None
    gyroscope = None
    camera = None
    base = None
    distanceSensors = None
    display = None
    __JointMotors = {}
    __Leds = {}
    speaker = None

    def __init__(self):
        Thread.__init__(self)
        try:
            subprocess.Popen("aprilTag.py", shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            print("Error aprilTag.py", e)
        try:
            subprocess.Popen("emotionrecognition2.py", shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            print("Error aprilTag.py", e)
        # Remote object connection for EmotionRecognition
        self.__emotionrecognition_proxy = connectComponent("emotionrecognition:tcp -h localhost -p 10006", RoboCompEmotionRecognition.EmotionRecognitionPrx)
        # Remote object connection for AprilTag
        self.__apriltagProxy = connectComponent("apriltag:tcp -h localhost -p 25000", RoboCompApriltag.ApriltagPrx)
        # self.start()
        self.active = True

    def addJointMotor(self, _key, _JointMotor):
        if _key in self.__JointMotors:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_JointMotor, JointMotor):
            raise Exception("_JointMotor is of type "+ type(_JointMotor) + " and must be of type JointMotor")
        else:
            self.__JointMotors[_key] = _JointMotor

    def addLed(self, _key, _Led):
        if _key in self.__Leds:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_Led, Led):
            raise Exception("_JointMotor is of type "+ type(_Led) + " and must be of type Led")
        else:
            self.__Leds[_key] = _Led

    def __detectAprilTags(self):
        if not self.__apriltag_current_exist:
            img = self.camera.getImage()
            frame = RoboCompApriltag.TImage()
            frame.width = img.shape[0]
            frame.height = img.shape[1]
            frame.depth = img.shape[2]
            frame.image = np.fromstring(img, np.uint8)
            aprils = self.__apriltagProxy.processimage(frame)
            print(aprils)
            self.__apriltag_current_exist = True
            self.__listAprilIDs = [a.id for a in aprils]

    def run(self):
        while self.active:
            if self.acelerometer is not None:
                self.acelerometer.read()
            if self.gyroscope is not None:
                self.gyroscope.read()
            if self.camera is not None:
                self.camera.read()
                self.__apriltag_current_exist = False
                self.__emotion_current_exist = False
            if self.distanceSensors is not None:
                self.distanceSensors.read()
            time.sleep(0.002)

    def lookingLabel(self, id):
        self.__detectAprilTags()
        return id in self.__listAprilIDs

    def stop(self):
        self.__stop_event.set()
        subprocess.Popen("killall -9 emotionrecognition2.py aprilTag.py", shell=True, stdout=subprocess.PIPE)

    def stopped(self):
        return self.__stop_event.is_set()

    def getSonars(self):
        if isinstance(self.distanceSensors, DistanceSensors):
            return self.distanceSensors.get()

    def getImage(self):
        if isinstance(self.camera, Camera):
            return self.camera.getImage()

    def getPose(self):
        raise NotImplementedError("To do")

    def setBaseSpeed(self, vAdvance, vRotation):
        if isinstance(self.base, Base):
            self.base.move(vAdvance, vRotation)

    def getAdv(self):
        if isinstance(self.base, Base):
            return self.base.adv()

    def getRot(self):
        if isinstance(self.base, Base):
            return self.base.rot()

    def express(self, _key):
        if isinstance(self.display, Display):
            print("express", _key)
            self.__currentEmotion = _key
            self.display.setEmotion(_key)

    def showImage(self, _img):
        if isinstance(self.display, Display):
            self.display.setImage(_img)

    def setJointAngle(self, _key, _angle):
        if _key in self.__JointMotors:
            self.__JointMotors.get(_key).sendAngle(_angle)
        # else:
        #     raise Exception("The key don't exist JointMotors")

    def setLedState(self, _key, _status):
        if _key in self.__Leds:
            self.__Leds.get(_key).setState(_status)
        # else:
        #     raise Exception("The key don't exist Leds")

    def getCurrentEmotion(self):
        return self.__currentEmotion

    def getAcelerometer(self):
        if isinstance(self.acelerometer, Acelerometer):
            return self.acelerometer.get()
        else:
            return None

    def getGyroscope(self):
        if isinstance(self.gyroscope, Gyroscope):
            return self.gyroscope.get()
        else:
            return None

    def speakText(self,_text):
        if isinstance(self.speaker, Speaker):
            self.speaker.sendText(_text)

    def sendAudio(self, _audioData):
        if isinstance(self.speaker, Speaker):
            self.speaker.sendAudio(_audioData)

    def getEmotions(self):
        if not self.emotion_current_exist:
            img = self.camera.getImage()
            frame = RoboCompEmotionRecognition.TImage()
            frame.width = img.shape[0]
            frame.height = img.shape[1]
            frame.depth = img.shape[2]
            frame.image = np.fromstring(img, np.uint8)
            self.currents_emotions = self.__emotionrecognition_proxy.processimage(frame)
            self.emotion_current_exist = True
        return self.currents_emotions

    def __del__(self):
            self.active = False

def addFunctions(_dictFuntions):
    for k, v in iter(_dictFuntions.items()):
        exec("Client.%s = v" % (k))
