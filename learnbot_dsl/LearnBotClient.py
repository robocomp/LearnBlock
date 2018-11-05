#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import sys, traceback, Ice, os, math, time, json, ast, copy, threading, json, cv2, urllib
from collections import namedtuple
import numpy as np

ROBOCOMP = ''
try:
    ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
    print('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
    ROBOCOMP = os.path.join('opt', 'robocomp')


ICEs = ["RGBD.ice", "Laser.ice", "DifferentialRobot.ice", "JointMotor.ice", "GenericBase.ice", "Display.ice", "Apriltag.ice","EmotionRecognition.ice" ]

icePaths = []
icePaths.append(os.path.join(os.path.dirname(__file__), "interfaces"))
imgPaths = os.path.join(os.path.dirname(os.path.realpath(__file__)),'imgs')
for ice in ICEs:
    for p in icePaths:
        if os.path.isfile(os.path.join(p, ice)):
            wholeStr = ' -I' + p + " --all "+os.path.join(p, ice)
            Ice.loadSlice(wholeStr)
            break

import RoboCompRGBD
import RoboCompLaser
import RoboCompDifferentialRobot
import RoboCompJointMotor
import RoboCompGenericBase
import RoboCompDisplay
import RoboCompApriltag
import RoboCompEmotionRecognition


import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

ic = None



class Client(Ice.Application, threading.Thread):

    def __init__(self, argv):
        threading.Thread.__init__(self)

        self.adv = 0
        self.rot = 0
        self.max_rot= 0.4
        self.image = np.zeros((240,320,3), np.uint8)
        self.usList = [1000]*7
        self.lasers_proxys=[]
        self.angleCamera = 0
        self.emotion_current_exist = False
        global ic

        params = copy.deepcopy(sys.argv)
        if len(params) > 1:
            if not params[1].startswith('--Ice.Config='):
                params[1] = '--Ice.Config=' + params[1]
        elif len(params) == 1:
            params.append('--Ice.Config=config')
        ic = Ice.initialize(params)


        status = 0
        try:
            # Remote object connection for DifferentialRobot
            try:
                proxyString = ic.getProperties().getProperty('DifferentialRobotProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.differentialrobot_proxy = RoboCompDifferentialRobot.DifferentialRobotPrx.checkedCast(basePrx)
                    print("Connection Successful: ",proxyString)
                except Ice.Exception:
                    print('Cannot connect to the remote object (DifferentialRobot)', proxyString)
                    raise
            except Ice.Exception as e:
                print(e)
                print('Cannot get DifferentialRobotProxy property.')
                raise


            # Remote object connection for Lasers

            for i in range(2, 7):
                try:
                    proxyString = ic.getProperties().getProperty('Laser' + str(i) + 'Proxy')
                    try:
                        basePrx = ic.stringToProxy(proxyString)
                        self.lasers_proxys.append(RoboCompLaser.LaserPrx.checkedCast(basePrx))
                        print("Connection Successful: ", proxyString)
                    except Ice.Exception:
                        print('Cannot connect to the remote object (Laser)', i, proxyString)
                        raise
                except Ice.Exception as e:
                    print(e)
                    print('Cannot get Laser', i, 'Proxy property.')
                    raise
            # Remote object connection for Display
            try:
                proxyString = ic.getProperties().getProperty('DisplayProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.display_proxy = RoboCompDisplay.DisplayPrx.checkedCast(basePrx)
                    print("Connection Successful: ", proxyString)
                except Ice.Exception:
                    print('Cannot connect to the remote object (Display)', proxyString)
                    raise
            except Ice.Exception as e:
                print(e)
                print('Cannot get DisplayProxy Proxy property.')
                raise

            # Remote object connection for RGBD
            try:
                proxyString = ic.getProperties().getProperty('RGBDProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.rgbd_proxy = RoboCompRGBD.RGBDPrx.checkedCast(basePrx)
                    print("Connection Successful: ",proxyString)
                except Ice.Exception:
                    print('Cannot connect to the remote object (RGBD)', proxyString)
                    raise
            except Ice.Exception as e:
                print(e)
                print('Cannot get RGBDProxy property.')
                raise
            # Remote object connection for JointMotor
            try:
                proxyString = ic.getProperties().getProperty('JointMotorProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.jointmotor_proxy = RoboCompJointMotor.JointMotorPrx.checkedCast(basePrx)
                    print("Connection Successful: ",proxyString)
                except Ice.Exception:
                    print('Cannot connect to the remote object (JointMotor)', proxyString)
                    raise
            except Ice.Exception as e:
                print(e)
                print('Cannot get JointMotorPrx property.')
                raise
            # Remote object connection for AprilTag
            try:
                proxyString = ic.getProperties().getProperty('ApriltagProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.apriltagProxy = RoboCompApriltag.ApriltagPrx.checkedCast(basePrx)
                    print("Connection Successful: ", proxyString)
                except Ice.Exception:
                    print('Cannot connect to the remote object (Apriltag)', proxyString)
                    raise
            except Ice.Exception as e:
                print(e)
                print('Cannot get JointMotorPrx property.')
                raise
            # Remote object connection for EmotionRecognition
            try:
                proxyString = ic.getProperties().getProperty('EmotionRecognition')
                i = 0
                try:
                    while(True):
                        try:
                            i += 1
                            basePrx = ic.stringToProxy(proxyString)
                            self.emotionrecognition_proxy = RoboCompEmotionRecognition.EmotionRecognitionPrx.checkedCast(basePrx)
                            break
                        except Ice.Exception:
                            if i is 4:
                                raise
                            else:
                                print("try ", i)
                                time.sleep(1.5)
                except Ice.Exception:
                    print('Cannot connect to the remote object (EmotionRecognition)', proxyString)
                    raise
            except Ice.Exception as e:
                print(e)
                print('Cannot get EmotionRecognition property.')
                raise
        except Ice.Exception as e:
                print("Error")
                traceback.print_exc()
                raise
        self._stop_event = threading.Event()
        self.apriltag_current_exist = False
        self.listIDs = []
        self.active = True
        self.start()

    def __detectAprilTags(self):
        if not self.apriltag_current_exist:
            frame = RoboCompApriltag.TImage()
            frame.width = self.image.shape[0]
            frame.height = self.image.shape[1]
            frame.depth = self.image.shape[2]
            frame.image = np.fromstring(self.image, np.uint8)
            aprils = self.apriltagProxy.processimage(frame)
            self.apriltag_current_exist = True
            self.listIDs = [a.id for a in aprils]

    def run(self):
        while self.active:
            try:
                self.apriltag_current_exist = False
                self.emotion_current_exist = False
                self.color, self.depth, self.headState, self.baseState = self.rgbd_proxy.getData()
                if (len(self.color) == 0) or (len(self.depth) == 0):
                        print('Error retrieving images!')
            except Ice.Exception:
                traceback.print_exc()

            self.readSonars()
            self.image = np.fromstring(self.color, dtype=np.uint8).reshape((240, 320, 3))

            time.sleep(0.01)

    def lookingLabel(self, id):
        self.__detectAprilTags()
        return id in self.listIDs

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def readSonars(self):
        for i in range(len(self.lasers_proxys)):
            lp = self.lasers_proxys[i]
            ldata = lp.getLaserData()
            self.usList[i] = min([x.dist for x in ldata])

    def getSonars(self):
        return self.usList

    def getImage(self):
        return self.image

    def getPose(self):
        x, y, alpha = self.differentialrobot_proxy.getBasePose()
        return x, y, alpha

    def setRobotSpeed(self, vAdvance=0, vRotation=0):
        try:
            self.adv = vAdvance
            self.rot = vRotation
            self.differentialrobot_proxy.setSpeedBase(-self.adv*8, self.rot*15)
        except Exception as e:
            print("Error setRobotSpeed")

    def setRobotSpeed(self, vAdvance=0, vRotation=0):
        if vAdvance!=0 or vRotation!=0:
            self.adv = vAdvance
            self.rot = vRotation
        self.differentialrobot_proxy.setSpeedBase(self.adv, self.rot)

    def expressFear(self):
        self.display_proxy.setImageFromFile(
            os.path.join(imgPaths,"miedo.png"))

    def expressSurprise(self):
        self.display_proxy.setImageFromFile(
            os.path.join(imgPaths,"sorpresa.png"))

    def expressAnger(self):
        self.display_proxy.setImageFromFile(
            os.path.join(imgPaths,"ira.png"))

    def expressSadness(self):
        self.display_proxy.setImageFromFile(
            os.path.join(imgPaths,"tristeza.png"))

    def expressDisgust(self):
        self.display_proxy.setImageFromFile(
            os.path.join(imgPaths,"asco.png"))

    def expressJoy(self):
        self.display_proxy.setImageFromFile(
            os.path.join(imgPaths,"alegria.png"))

    def expressNeutral(self):
        self.display_proxy.setImageFromFile(
            os.path.join(imgPaths,"SinEmocion2.png"))

    def setJointAngle(self, angle):
        self.angleCamera = angle
        goal = RoboCompJointMotor.MotorGoalPosition()
        goal.name = 'servo'
        goal.position = -angle
        self.jointmotor_proxy.setPosition(goal)

    def getEmotions(self):
        if not self.emotion_current_exist:
            frame = RoboCompEmotionRecognition.TImage()
            frame.width = self.image.shape[0]
            frame.height = self.image.shape[1]
            frame.depth = self.image.shape[2]
            frame.image = np.fromstring(self.image, np.uint8)
            self.currents_emotions = self.emotionrecognition_proxy.processimage(frame)
            self.emotion_current_exist = True
        return self.currents_emotions

    def __del__(self):
            self.active = False
