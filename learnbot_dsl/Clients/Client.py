#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
from threading import Thread, Lock, Event
import numpy as np, copy, sys, time, Ice, os, subprocess
from learnbot_dsl.Clients.Devices import *
from learnbot_dsl import PATHINTERFACES
from datetime import timedelta
from learnbot_dsl.functions import getFuntions

__ICEs = ["EmotionRecognition.ice", "Apriltag.ice" ]
__icePaths = []
path = os.path.dirname(os.path.realpath(__file__))
__icePaths.append(os.path.join(os.path.dirname(path), "interfaces"))
__icePaths.append(PATHINTERFACES)
for ice in __ICEs:
    for p in __icePaths:
        if os.path.isfile(os.path.join(p, ice)):
            wholeStr = ' -I' + p + " --all " + os.path.join(p, ice)
            Ice.loadSlice(wholeStr)
            break

import RoboCompEmotionRecognition
import RoboCompApriltag


def connectComponent(stringProxy, _class, tries=4):
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
            if i is tries:
                print("Cannot connect to the proxy: ", stringProxy)
                return None
            else:
                time.sleep(1.5)
    return proxy

class Client(Thread):

    requiementFunctions = []

    def __new__(cls, *args, **kwargs):
        if len(cls.requiementFunctions) is not 0:
            functions = getFuntions()
            map(lambda x: setattr(Client, x, functions[x]),cls.requiementFunctions)
        instance = super(Client, cls).__new__(cls, *args, **kwargs)
        return instance

    def __init__(self,_miliseconds=100):
        Thread.__init__(self)
        self.__stop_event = Event()

        # Variables of Emotion Recognition
        self.__emotion_current_exist = False
        self.__currents_emotions = []
        self.__currentEmotion = Emotions.NoneEmotion
        self.__JointMotors = {}
        self.__Leds = {}
        # Variables of AprilTag
        self.__apriltag_current_exist = False
        self.__listAprilIDs = []

        self.__period = timedelta(milliseconds=_miliseconds)
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
        if not self.__apriltag_current_exist and hasattr(self, "camera"):
            img = self.camera.getImage()
            frame = RoboCompApriltag.TImage()
            frame.width = img.shape[0]
            frame.height = img.shape[1]
            frame.depth = img.shape[2]
            frame.image = np.fromstring(img, np.uint8)
            aprils = self.__apriltagProxy.processimage(frame)
            self.__apriltag_current_exist = True
            self.__listAprilIDs = [a.id for a in aprils]

    def __readDevices(self):
        if hasattr(self, "acelerometer"):
            self.acelerometer.read()
        if hasattr(self, "gyroscope"):
            self.gyroscope.read()
        if hasattr(self, "camera"):
            self.camera.read()
            self.__apriltag_current_exist = False
            self.__emotion_current_exist = False
        if hasattr(self, "distanceSensors"):
            self.distanceSensors.read()

    def run(self):
        self.__readDevices()
        while not self.__stop_event.wait(self.__period.total_seconds()):
            self.__readDevices()

    def lookingLabel(self, id):
        time.sleep(0)
        self.__detectAprilTags()
        return id in self.__listAprilIDs

    def stop(self):
        self.__stop_event.set()
        subprocess.Popen("killall -9 emotionrecognition2.py aprilTag.py", shell=True, stdout=subprocess.PIPE)
        self.join()

    def stopped(self):
        return self.__stop_event.is_set()

    def getSonars(self):
        if hasattr(self, "distanceSensors"):
            time.sleep(0)
            return self.distanceSensors.get()

    def getImage(self):
        if hasattr(self, "camera"):
            time.sleep(0)
            return self.camera.getImage()

    def getPose(self):
        time.sleep(0)
        raise NotImplementedError("To do")

    def setBaseSpeed(self, vAdvance, vRotation):
        if hasattr(self, "base"):
            time.sleep(0)
            self.base.move(vAdvance, vRotation)

    def getAdv(self):
        if hasattr(self, "base"):
            time.sleep(0)
            return self.base.adv()

    def getRot(self):
        if hasattr(self, "base"):
            time.sleep(0)
            return self.base.rot()

    def express(self, _key):
        if hasattr(self, "display"):
            time.sleep(0)
            self.__currentEmotion = _key
            self.display.setEmotion(_key)

    def showImage(self, _img):
        if hasattr(self, "display"):
            time.sleep(0)
            self.display.setImage(_img)

    def setJointAngle(self, _key, _angle):
        if _key in self.__JointMotors:
            time.sleep(0)
            self.__JointMotors.get(_key).sendAngle(_angle)
        # else:
        #     raise Exception("The key don't exist JointMotors")

    def setLedState(self, _key, _status):
        if _key in self.__Leds:
            time.sleep(0)
            self.__Leds.get(_key).setState(_status)
        # else:
        #     raise Exception("The key don't exist Leds")

    def getCurrentEmotion(self):
        time.sleep(0)
        return self.__currentEmotion

    def getAcelerometer(self):
        if hasattr(self, "acelerometer"):
            time.sleep(0)
            return self.acelerometer.get()

    def getGyroscope(self):
        if hasattr(self, "gyroscope"):
            time.sleep(0)
            return self.gyroscope.get()

    def speakText(self,_text):
        if hasattr(self, "speaker"):
            time.sleep(0)
            self.speaker.sendText(_text)

    def sendAudio(self, _audioData):
        if hasattr(self, "speaker"):
            time.sleep(0)
            self.speaker.sendAudio(_audioData)

    def getEmotions(self):
        if not self.emotion_current_exist and hasattr(self, "camera"):
            time.sleep(0)
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

