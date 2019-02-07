#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
from threading import Thread, Lock, Event
import numpy as np, copy, sys, time, Ice, os, subprocess
from enum import Enum

__ICEs = ["EmotionRecognition.ice", "Apriltag.ice" ]
__icePaths = []
__icePaths.append(os.path.join(os.path.dirname(__file__), "interfaces"))
for ice in __ICEs:
    for p in __icePaths:
        if os.path.isfile(os.path.join(p, ice)):
            wholeStr = ' -I' + p + " --all " + os.path.join(p, ice)
            Ice.loadSlice(wholeStr)
            break

import RoboCompEmotionRecognition
import RoboCompApriltag

class Emotions(Enum):
    NoneEmotion = -1
    Fear = 0
    Surprise = 1
    Anger = 2
    Sadness = 3
    Disgust = 4
    Joy = 5
    Neutral = 7

class Device():
    __available = False
    __readDevice = None
    __callDevice = None
    def setAvailable(self, _available):
        self.__available = _available

    def isAvailable(self):
        return self.__available

class Acelerometer(Device):
    '''
    Acelerometer is a class that contain the values rx, ry, rz of a Acelerometer in rad.
    '''
    x = None
    y = None
    z = None
    def __init__(self, _readFunction):
        self.__readDevice = _readFunction
        
    def set(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z
        
    def read(self):
        _x, _y, _z = self.__readDevice()
        self.set(_x, _y, _z)
        
class Gyroscope(Device):
    '''
    Gyroscope is a class that contain the values rx, ry, rz of a Gyroscope in rad.
    '''
    rx = None
    ry = None
    rz = None
    def __init__(self, _readFunction):
        self.__readDevice = _readFunction
        
    def set(self, _rx, _ry, _rz):
        self.rx = _rx
        self.ry = _ry
        self.rz = _rz
        
    def read(self):
        _rx, _ry, _rz = self.__readDevice()
        self.set(_rx, _ry, _rz)

class Camera(Device):
    '''
    Camera devices.
    '''
    __image = np.zeros((240, 320, 3), np.uint8)     # RGB image
    __newImageAvailable = False
    __mutexRead = Lock()
    def __init__(self, _readFunction):
        self.__readDevice = _readFunction

    def read(self):
        self.__mutexRead.acquire()
        img, new = self.__readDevice()
        if new is True:
            self.__image = img
            self.__newImageAvailable = True
        self.__mutexRead.release()

    def getImage(self):
        self.__mutexRead.acquire()
        simage = copy.copy(self.__image)
        self.__mutexRead.release()
        return simage

class DistanceSensors(Device):
    __distanceSensor = {"front": [1000, 1000, 1000],  # The values must be in mm
                        "left": [1000, 1000],
                        "right": [1000, 1000],
                        "back": None,
                        "bottom": None}
    def __init__(self, _readFunction):
        self.__readDevice = _readFunction
    
    def set(self, key, values):
        self.__distanceSensor[key] = values
    
    def read(self):
        dictValues = self.__readDevice()
        for key in dictValues:
            self.set(key, dictValues[key])
    def get(self):
        return self.__distanceSensor
        
class Base(Device):
    __adv = 0       # in mm
    __rot = 0       # in rad
    __max_rot = 0   # in rad

    def __init__(self, _callFunction, _max_rot):
        self.__callDevice = _callFunction
        self.__max_rot = _max_rot
    
    def move(self, _adv, _rot):
        self.__callDevice(_adv, _rot)
    
    def adv(self):
        return self.__adv
    
    def rot(self):
        return self.__rot

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
    def __init__(self):
        Thread.__init__(self)
        # self.__acelerometer = Acelerometer(_readFunction=f)
        # self.__gyroscope = Gyroscope(_readFunction=f)
        # self.__camera = Camera(_readFunction=f)
        # self.__base = Base(_callFunction=f)
        # self.__distanceSensors = DistanceSensors(_readFunction=f)

        subprocess.Popen("aprilTag.py", shell=True, stdout=subprocess.PIPE)
        subprocess.Popen("emotionrecognition2.py", shell=True, stdout=subprocess.PIPE)
        # Remote object connection for EmotionRecognition
        self.__emotionrecognition_proxy = connectComponent("emotionrecognition:tcp -h localhost -p 10006", RoboCompEmotionRecognition.EmotionRecognitionPrx)
        # Remote object connection for AprilTag
        self.__apriltagProxy = connectComponent("apriltag:tcp -h localhost -p 25000", RoboCompApriltag.ApriltagPrx)
        # self.start()
        self.active = True

    def __detectAprilTags(self):
        if not self.__apriltag_current_exist:
            img = self.camera.getImage()
            frame = RoboCompApriltag.TImage()
            frame.width = img.shape[0]
            frame.height = img.shape[1]
            frame.depth = img.shape[2]
            frame.image = np.fromstring(img, np.uint8)
            aprils = self.__apriltagProxy.processimage(frame)
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
        return self.distanceSensors.get()

    def getImage(self):
        return self.camera.getImage()

    def getPose(self):
        raise NotImplementedError("To do")

    def setRobotSpeed(self, vAdvance=0, vRotation=0):
        self.base.move(vAdvance, vRotation)

    def expressJoy(self):
        raise NotImplementedError("To be implemented")

    def expressSadness(self):
        raise NotImplementedError("To be implemented")

    def expressSurprise(self):
        raise NotImplementedError("To be implemented")

    def expressFear(self):
        raise NotImplementedError("To be implemented")

    def expressAnger(self):
        raise NotImplementedError("To be implemented")

    def expressDisgust(self):
        raise NotImplementedError("To be implemented")

    def expressNeutral(self):
        raise NotImplementedError("To be implemented")

    def setJointAngle(self, angle):
        raise NotImplementedError("To be implemented")

    def getCurrentEmotion(self):
        return self.__currentEmotion

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
