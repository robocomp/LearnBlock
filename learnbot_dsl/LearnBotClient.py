#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, traceback, Ice, os, math, time, json, ast, copy, threading
import json
import cv2
import urllib
from collections import namedtuple
import numpy as np

ROBOCOMP = ''
try:
    ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
    print '$ROBOCOMP environment variable not set, using the default value /opt/robocomp'
    ROBOCOMP = '/opt/robocomp'

preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"

Ice.loadSlice(preStr+"RGBD.ice")
Ice.loadSlice(preStr+"Laser.ice")
Ice.loadSlice(preStr+"DifferentialRobot.ice")
Ice.loadSlice(preStr+"JointMotor.ice")
Ice.loadSlice(preStr+"GenericBase.ice")
Ice.loadSlice(preStr+"Display.ice")


import RoboCompRGBD
import RoboCompLaser
import RoboCompDifferentialRobot
import RoboCompJointMotor
import RoboCompGenericBase
import RoboCompDisplay

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
        global ic

        params = copy.deepcopy(sys.argv)
        if len(params) > 1:
            if not params[1].startswith('--Ice.Config='):
                params[1] = '--Ice.Config=' + params[1]
        elif len(params) == 1:
            params.append('--Ice.Config=config')
        print params
        ic = Ice.initialize(params)


        status = 0
        try:
            # Remote object connection for DifferentialRobot
            try:
                proxyString = ic.getProperties().getProperty('DifferentialRobotProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.differentialrobot_proxy = RoboCompDifferentialRobot.DifferentialRobotPrx.checkedCast(basePrx)
                    print "Connection Successful: ",proxyString
                except Ice.Exception:
                    print 'Cannot connect to the remote object (DifferentialRobot)', proxyString
                    sys.exit(1)
            except Ice.Exception, e:
                print e
                print 'Cannot get DifferentialRobotProxy property.'
                sys.exit(1)


            # Remote object connection for Lasers

            for i in range(1, 8):
                try:
                    proxyString = ic.getProperties().getProperty('Laser' + str(i) + 'Proxy')
                    try:
                        basePrx = ic.stringToProxy(proxyString)
                        self.lasers_proxys.append(RoboCompLaser.LaserPrx.checkedCast(basePrx))
                        print "Connection Successful: ", proxyString
                    except Ice.Exception:
                        print 'Cannot connect to the remote object (Laser)', proxyString
                        sys.exit(1)
                except Ice.Exception, e:
                    print e
                    print 'Cannot get Laser', i, 'Proxy property.'
                    sys.exit(1)

            # Remote object connection for Display
            try:
                proxyString = ic.getProperties().getProperty('DisplayProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.display_proxy = RoboCompDisplay.DisplayPrx.checkedCast(basePrx)
                    print "Connection Successful: ", proxyString
                except Ice.Exception:
                    print 'Cannot connect to the remote object (Laser)', proxyString
                    sys.exit(1)
            except Ice.Exception, e:
                print e
                print 'Cannot get Laser', i, 'Proxy property.'
                sys.exit(1)

            # Remote object connection for RGBD
            try:
                proxyString = ic.getProperties().getProperty('RGBDProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.rgbd_proxy = RoboCompRGBD.RGBDPrx.checkedCast(basePrx)
                    print "Connection Successful: ",proxyString
                except Ice.Exception:
                    print 'Cannot connect to the remote object (RGBD)', proxyString
                    sys.exit(1)
            except Ice.Exception, e:
                print e
                print 'Cannot get RGBDProxy property.'
                sys.exit(1)
        except:
                print "Error"
                traceback.print_exc()
                sys.exit(1)

        self.active = True
        self.start()

    def run(self):
        while self.active:
            try:
                self.color, self.depth, self.headState, self.baseState = self.rgbd_proxy.getData()
                if (len(self.color) == 0) or (len(self.depth) == 0):
                        print 'Error retrieving images!'
            except Ice.Exception:
                traceback.print_exc()

            self.readSonars()
            self.image = np.fromstring(self.color, dtype=np.uint8).reshape((240, 320, 3))

            time.sleep(0.01)

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
        if vAdvance!=0 or vRotation!=0:
            self.adv = vAdvance
            self.rot = vRotation
        self.differentialrobot_proxy.setSpeedBase(self.adv,self.rot)

    def expressFear(self):
        self.display_proxy.setImageFromFile(
            "/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/miedo.png")

    def expressSurprise(self):
        self.display_proxy.setImageFromFile(
            "/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/sorpresa.png")

    def expressAnger(self):
        self.display_proxy.setImageFromFile(
            "/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/ira.png")

    def expressSadness(self):
        self.display_proxy.setImageFromFile(
            "/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/tristeza.png")

    def expressDisgust(self):
        self.display_proxy.setImageFromFile(
            "/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/asco.png")

    def expressJoy(self):
        print "expressJoy"
        self.display_proxy.setImageFromFile(
            "/home/robocomp/robocomp/components/learnbot/components/emotionalMotor/imgs/alegria.png")


    def __del__(self):
            self.active = False
