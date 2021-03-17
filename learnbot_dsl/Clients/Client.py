#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
from threading import Thread, Lock, Event
import numpy as np, copy, sys, time, os, subprocess, json
from learnbot_dsl.Clients.Devices import *
from learnbot_dsl import PATHINTERFACES
from datetime import timedelta
from learnbot_dsl.functions import getFuntions
from learnbot_dsl.learnbotCode import getAprilTextDict

global IceLoaded

try:
    import Ice
    IceLoaded = True
except ImportError as e:
    IceLoaded = False

if IceLoaded:    
    __ICEs = ["EmotionRecognition.ice", "Apriltag.ice" ]
    __icePaths = []
    path = os.path.dirname(os.path.realpath(__file__))
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

class MetaClient(type):
    def __call__(cls, *args, **kwargs):
        print("__call__")
        obj = cls.__new__(cls, *args, **kwargs)
        if "availableFunctions" in kwargs:
            del kwargs["availableFunctions"]
        obj.__init__(*args, **kwargs)
        return obj

class Client(Thread, metaclass=MetaClient):

    def __new__(cls, *args, **kwargs):
        print("__new__")
        usedFuncts = []
        if "availableFunctions" in kwargs:
            usedFuncts = kwargs.pop('availableFunctions')
        print("availableFunctions", usedFuncts)
        functions = getFuntions()
        for k, v in iter(functions.items()):
            if not usedFuncts or k in usedFuncts:
#            if v["type"] in cls.devicesAvailables + ["basics"]:
                print("add ", k, v["type"])
                setattr(Client, k, v["function"])
        instance = super(Client, cls).__new__(cls, *args, **kwargs)
        return instance

    def __init__(self,_miliseconds=100):
        print("__init__")
        Thread.__init__(self)
        self.__stop_event = Event()

        # Variables of Emotion Recognition
        self.__emotion_current_exist = False
        self.__current_emotions = []
        self.__currentEmotion = Emotions.NoneEmotion
        self.__Acelerometers = {}
        self.__Bases = {}
        self.__Cameras = {}
        self.__Displays = {}
        self.__DistanceSensors = {}
        self.__GroundSensors = {}
        self.__Gyroscopes = {}
        self.__JointMotors = {}
        self.__Leds = {}
        self.__Speakers = {}
        # Variables of AprilTag
        self.__apriltag_current_exist = False
        self.__listAprilIDs = []
        self.__posAprilTags = {}
        self.aprilTextDict = getAprilTextDict()

        self.__apriltagRunning = False
        self.__emotionRecRunning = False

        self.__period = timedelta(milliseconds=_miliseconds)

    def __launchComponents(self):
        global IceLoaded

        if IceLoaded:
            try:
                subprocess.Popen("aprilTag.py", shell=True, stdout=subprocess.PIPE)
                self.__apriltagRunning = True
            except Exception as e:
                self.__apriltagRunning = False

            try:
                subprocess.Popen("emotionrecognition2.py", shell=True, stdout=subprocess.PIPE)
                self.__emotionRecRunning = True
            except Exception as e:
                self.__emotionRecRunning = False

            # Remote object connection for EmotionRecognition
            if self.__emotionRecRunning:
                self.__emotionrecognition_proxy = connectComponent("emotionrecognition:tcp -h localhost -p 10006", RoboCompEmotionRecognition.EmotionRecognitionPrx)
            # Remote object connection for AprilTag
            if self.__apriltagRunning:
                self.__apriltagProxy = connectComponent("apriltag:tcp -h localhost -p 25000", RoboCompApriltag.ApriltagPrx)


    def disconnect(self):
        raise NotImplementedError()

    def addAcelerometer(self, _Acelerometer, _key = "ROBOT"):

        if _key in self.__Acelerometers:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_Acelerometer, Acelerometer):
            raise Exception("_Acelerometer is of type "+ type(_Acelerometer) + " and must be of type Acelerometer")
        else:
            self.__Acelerometers[_key] = _Acelerometer

    def addBase(self, _Base, _key = "ROBOT"):

        if _key in self.__Bases:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_Base, Base):
            raise Exception("_Base is of type "+ type(_Base) + " and must be of type Base")
        else:
            self.__Bases[_key] = _Base

    def addCamera(self, _Camera, _key = "ROBOT"):

        if _key in self.__Cameras:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_Camera, Camera):
            raise Exception("_Camera is of type "+ type(_Camera) + " and must be of type Camera")
        else:
            self.__Cameras[_key] = _Camera
            if not self.__apriltagRunning or not self.__emotionRecRunning:
                self.__launchComponents()


    def addDisplay(self, _Display, _key = "ROBOT"):

        if _key in self.__Displays:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_Display, Display):
            raise Exception("_Display is of type "+ type(_Display) + " and must be of type Display")
        else:
            self.__Displays[_key] = _Display

    def addDistanceSensors(self, _DistanceSensors, _key = "ROBOT"):

        if _key in self.__DistanceSensors:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_DistanceSensors, DistanceSensors):
            raise Exception("_DistanceSensors is of type "+ type(_DistanceSensors) + " and must be of type DistanceSensors")
        else:
            self.__DistanceSensors[_key] = _DistanceSensors

    def addGroundSensors(self, _GroundSensors, _key = "ROBOT"):

        if _key in self.__GroundSensors:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_GroundSensors, GroundSensors):
            raise Exception("_GroundSensors is of type "+ type(_GroundSensors) + " and must be of type GroundSensors")
        else:
            self.__GroundSensors[_key] = _GroundSensors

    def addGyroscope(self, _Gyroscope, _key = "ROBOT"):

        if _key in self.__Gyroscopes:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_Gyroscope, Gyroscope):
            raise Exception("_Gyroscope is of type "+ type(_Gyroscope) + " and must be of type Gyroscope")
        else:
            self.__Gyroscopes[_key] = _Gyroscope


    def addJointMotor(self, _JointMotor, _key = "ROBOT"):

        if _key in self.__JointMotors:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_JointMotor, JointMotor):
            raise Exception("_JointMotor is of type "+ type(_JointMotor) + " and must be of type JointMotor")
        else:
            self.__JointMotors[_key] = _JointMotor

    def addLed(self, _Led, _key = "ROBOT"):
        if _key in self.__Leds:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_Led, Led):
            raise Exception("_JointMotor is of type "+ type(_Led) + " and must be of type Led")
        else:
            self.__Leds[_key] = _Led

    def addSpeaker(self, _Speaker, _key = "ROBOT"):

        if _key in self.__Speakers:
            raise Exception("The key " + _key + "already exist")
        elif not isinstance(_Speaker, Speaker):
            raise Exception("_Speaker is of type "+ type(_Speaker) + " and must be of type Speaker")
        else:
            self.__Speakers[_key] = _Speaker


    def __readDevices(self):
        if bool(self.__Acelerometers):
            for acelerometer in self.__Acelerometers.values():
                acelerometer.read()
        if bool(self.__Gyroscopes):
            for gyroscope in self.__Gyroscopes.values():
                gyroscope.read()
        if bool(self.__Cameras):
            for cam in self.__Cameras.values():
                cam.read()
            self.__apriltag_current_exist = False
            self.__emotion_current_exist = False
        if bool(self.__DistanceSensors):
            for distSensors in self.__DistanceSensors.values():
                distSensors.read()
        if bool(self.__GroundSensors):
            for groundSensors in self.__GroundSensors.values():
                groundSensors.read()


    def run(self):
        self.__readDevices()
        while not self.__stop_event.wait(self.__period.total_seconds()):
            self.__readDevices()
        self.disconnect()

    def stop(self):
        self.__stop_event.set()
        subprocess.Popen("pkill -f emotionrecognition2.py", shell=True, stdout=subprocess.PIPE)
        subprocess.Popen("pkill -f aprilTag.py", shell=True, stdout=subprocess.PIPE)

    def stopped(self):
        return self.__stop_event.is_set()

    def getDistanceSensors(self, _keyDS="ROBOT"):
        if _keyDS in self.__DistanceSensors:
            time.sleep(0)
            return self.__DistanceSensors[_keyDS].get()
        else:
            return None

    def getGroundSensors(self, _keyGS="ROBOT"):
        if _keyGS in self.__GroundSensors:
            time.sleep(0)
            return self.__GroundSensors[_keyGS].get()
        else:
            return None


    def getPose(self, _keyBase = "ROBOT"):
        time.sleep(0)
        raise NotImplementedError("To do")

    def setBaseSpeed(self, vAdvance, vRotation, _keyBase = "ROBOT"):
        if _keyBase in self.__Bases:
            time.sleep(0)
            self.__Bases[_keyBase].move(vAdvance, vRotation)

    def getAdv(self, _keyBase = "ROBOT"):
        if _keyBase in self.__Bases:
            time.sleep(0)
            return self.__Bases[_keyBase].adv()
        else:
            return None

    def getRot(self, _keyBase = "ROBOT"):
        if _keyBase in self.__Bases:
            time.sleep(0)
            return self.__Bases[_keyBase].rot()
        else:
            return None

    def express(self, _keyEmotion, _keyDisplay = "ROBOT"):
        if _keyDisplay in self.__Displays:
            time.sleep(0)
            self.__currentEmotion = _keyEmotion
            self.__Displays[_keyDisplay].setEmotion(_keyEmotion)

    def getCurrentEmotion(self):
        time.sleep(0)
        return self.__currentEmotion

    def showImage(self, _img, _keyDisplay = "ROBOT"):
        if _keyDisplay in self.__Displays:
            time.sleep(0)
            self.__Displays[_keyDisplay].setImage(_img)

    def setJointAngle(self, _angle, _keyJoint = "ROBOT"):
        if _keyJoint in self.__JointMotors:
            time.sleep(0)
            self.__JointMotors.get(_keyJoint).sendAngle(_angle)

    def setLedState(self, _status, _keyLed = "ROBOT"):
        if _keyLed in self.__Leds:
            time.sleep(0)
            self.__Leds.get(_keyLed).setState(_status)

    def getAcelerometer(self, _keyAcel = "ROBOT"):
        if _keyAcel in self.__Acelerometers:
            time.sleep(0)
            return self.__Acelerometers[_keyAcel].get()
        else:
            return None

    def getGyroscope(self, _keyGyro = "ROBOT"):
        if _keyGyro in self.__Gyroscopes:
            time.sleep(0)
            return self.__Gyroscopes[_keyGyro].get()
        else:
            return None

    def resetGyroscope(self, _keyGyro = "ROBOT"):
        if _keyGyro in self.__Gyroscopes:
            time.sleep(0)
            self.__Gyroscopes[_keyGyro].reset()

    def speakText(self,_text, _keySpeaker = "ROBOT"):
        if _keySpeaker in self.__Speakers:
            time.sleep(0)
            self.__Speakers[_keySpeaker].sendText(_text)

    def sendAudio(self, _audioData, _keySpeaker = "ROBOT"):
        if _keySpeaker in self.__Speakers:
            time.sleep(0)
            self.__Speakers[_keySpeaker].sendAudio(_audioData)

    def getImage(self, _keyCam = "ROBOT"):
        if _keyCam in self.__Cameras:
            time.sleep(0)
            return self.__Cameras[_keyCam].getImage()
        else:
            return None

    def __detectAprilTags(self, _keyCam = "ROBOT"):
        if _keyCam in self.__Cameras:
            if self.__apriltagRunning and not self.__apriltag_current_exist:
                img = self.__Cameras[_keyCam].getImage()
                frame = RoboCompApriltag.TImage()
                frame.width = img.shape[0]
                frame.height = img.shape[1]
                frame.depth = img.shape[2]
                frame.image = np.fromstring(img, np.uint8)
                aprils = self.__apriltagProxy.processimage(frame)
                self.__apriltag_current_exist = True
                self.__listAprilIDs = [a.id for a in aprils]
                self.__posAprilTags = {a.id : [a.cx, a.cy] for a in aprils}

    def lookingLabel(self, id, _keyCam="ROBOT"):
        time.sleep(0)
        if isinstance(id, str):
            if id in self.aprilTextDict:
                id = self.aprilTextDict[id]
            else:
                return False
        self.__detectAprilTags(_keyCam)
        return id in self.__listAprilIDs

    def getPosTag(self, id=None, _keyCam="ROBOT"):
        time.sleep(0)
        self.__detectAprilTags(_keyCam)
        if id is None:
            if len(self.__listAprilIDs)>0:
                return self.__posAprilTags[self.__listAprilIDs[0]]
            else:
                return None
        if id in self.__listAprilIDs:
            return self.__posAprilTags[id]
        else:
            return None

    def listTags(self, _keyCam="ROBOT"):
        self.__detectAprilTags(_keyCam)
        return self.__listAprilIDs

    def getEmotions(self, _keyCam = "ROBOT"):
        if self.__emotionRecRunning and not self.__emotion_current_exist and _keyCam in self.__Cameras:
            time.sleep(0)
            img = self.__Cameras[_keyCam].getImage()
            frame = RoboCompEmotionRecognition.TImage()
            frame.width = img.shape[0]
            frame.height = img.shape[1]
            frame.depth = img.shape[2]
            frame.image = np.fromstring(img, np.uint8)
            self.__current_emotions = self.__emotionrecognition_proxy.processimage(frame)
            self.__emotion_current_exist = True
        return self.__current_emotions

    def __del__(self):
            self.active = False

