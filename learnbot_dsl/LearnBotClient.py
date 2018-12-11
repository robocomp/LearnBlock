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

ICEs = ["RGBD.ice", "Laser.ice", "DifferentialRobot.ice", "JointMotor.ice", "GenericBase.ice", "Display.ice",
        "Apriltag.ice", "EmotionRecognition.ice"]

icePaths = []
icePaths.append(os.path.join(os.path.dirname(__file__), "interfaces"))
imgPaths = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'imgs')
for ice in ICEs:
    for p in icePaths:
        if os.path.isfile(os.path.join(p, ice)):
            wholeStr = ' -I' + p + " --all " + os.path.join(p, ice)
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
from PIL import Image, ImageDraw, ImageQt
import copy, json, tempfile, os

DEFAULTCONFIGNEUTRAL = {"cejaD": {"P2": {"y": 73, "x": 314}, "P3": {"y": 99, "x": 355}, "P1": {"y": 99, "x": 278}, "P4": {"y": 94, "x": 313}}, "parpadoI": {"P2": {"y": 80, "x": 160}, "P3": {"y": 151, "x": 214}, "P1": {"y": 151, "x": 112}, "P4": {"y": 80, "x": 160}}, "ojoI": {"Radio1": {"Value": 34}, "Center": {"y": 151, "x": 161}, "Radio2": {"Value": 34}}, "cejaI": {"P2": {"y": 73, "x": 160}, "P3": {"y": 99, "x": 201}, "P1": {"y": 99, "x": 122}, "P4": {"y": 94, "x": 160}}, "ojoD": {"Radio1": {"Value": 34}, "Center": {"y": 151, "x": 316}, "Radio2": {"Value": 34}}, "boca": {"P2": {"y": 231, "x": 239}, "P3": {"y": 234, "x": 309}, "P1": {"y": 234, "x": 170}, "P6": {"y": 242, "x": 170}, "P4": {"y": 242, "x": 309}, "P5": {"y": 241, "x": 239}}, "pupilaD": {"Radio": {"Value": 5}, "Center": {"y": 151, "x": 316}}, "lengua": {"P2": {"y": 238, "x": 239}, "P3": {"y": 238, "x": 309}, "P1": {"y": 238, "x": 199}, "P4": {"y": 238, "x": 273}}, "mejillaI": {"P2": {"y": 188, "x": 160}, "P3": {"y": 187, "x": 201}, "P1": {"y": 187, "x": 122}, "P4": {"y": 187, "x": 160}}, "parpadoD": {"P2": {"y": 80, "x": 314}, "P3": {"y": 151, "x": 369}, "P1": {"y": 151, "x": 266}, "P4": {"y": 80, "x": 313}}, "pupilaI": {"Radio": {"Value": 5}, "Center": {"y": 151, "x": 161}}, "mejillaD": {"P2": {"y": 188, "x": 314}, "P3": {"y": 187, "x": 355}, "P1": {"y": 187, "x": 278}, "P4": {"y": 187, "x": 313}}}

OFFSET = 0.06666666666666667


def bezier(p1, p2, t):
    diff = (p2[0] - p1[0], p2[1] - p1[1])
    return [p1[0] + diff[0] * t, p1[1] + diff[1] * t]


def getPointsBezier(points):
    bezierPoints = list()
    pointsCopy = copy.copy(points)
    for t in [x / 50. for x in range(51)]:
        while len(points) != 1:
            newPoints = list()
            p1 = points[0]
            for p2 in points[1:]:
                newPoints.append(bezier(p1, p2, t))
                p1 = p2
            points = newPoints
        bezierPoints.append(tuple(points[0]))
        points = pointsCopy
    return bezierPoints


def getBecierConfig(old_config, config_target, t):
    config = copy.copy(old_config)
    for parte in old_config:
        for point in old_config[parte]:
            if "Radio" in point:
                radio = bezier((old_config[parte][point]["Value"], 0), (config_target[parte][point]["Value"], 0), t)
                config[parte][point]["Value"] = radio[0]
            else:
                p = bezier((old_config[parte][point]["x"], old_config[parte][point]["y"]),
                           (config_target[parte][point]["x"], config_target[parte][point]["y"]), t)
                config[parte][point]["x"] = p[0]
                config[parte][point]["y"] = p[1]
    return config


class Face(threading.Thread):

    def __init__(self, display_proxy):
        threading.Thread.__init__(self)
        self.img = Image.new('RGB', (480, 320), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.img)
        self.config = DEFAULTCONFIGNEUTRAL
        self.old_config = DEFAULTCONFIGNEUTRAL
        self.t = 0.9
        self.config_target = DEFAULTCONFIGNEUTRAL
        self.display_proxy = display_proxy
        # self.mutex = threading.Lock()
        # path = self.render()
        # self.display_proxy.setImageFromFile(path)

    def run(self):
        while True:
            path = self.render()
            if path is not None:
                self.display_proxy.setImageFromFile(path)

    def render(self):
        if self.t <= 1 and self.config_target is not None:
            # with self.mutex:
            #     old_config = copy.copy(self.old_config)
            #     config_target = copy.copy(self.config_target)
            #     t = copy.copy(self.t)
            #     self.t += OFFSET
            # config = getBecierConfig(old_config, config_target, t)
            # with self.mutex:
            #     self.config = copy.copy(config)
            config = self.config = getBecierConfig(self.old_config, self.config_target, self.t)
            self.t += OFFSET
            self.draw.rectangle(((0, 0), (479, 319)), fill=(255, 255, 255), outline=(255, 255, 255))
            self.renderOjo(config["ojoI"])
            self.renderOjo(config["ojoD"])
            self.renderParpado(config["parpadoI"])
            self.renderParpado(config["parpadoD"])
            self.renderCeja(config["cejaI"])
            self.renderCeja(config["cejaD"])
            self.renderBoca(config["boca"])
            self.renderPupila(config["pupilaI"])
            self.renderPupila(config["pupilaD"])
            self.renderMejilla(config["mejillaI"])
            self.renderMejilla(config["mejillaD"])
            self.renderLengua(config["lengua"])
            # path = "/dev/fb0"
            # with open(path, "wb") as f:
            #     f.write(self.img.tobytes())

            img = np.array(self.img)
            img = cv2.flip(img, 1)
            cv2.imwrite("/tmp/ebofaceimg.png",img)
            return "/tmp/ebofaceimg.png"
        elif self.config_target is not None:
            # with self.mutex:
            self.old_config = self.config_target
            self.config_target = None
        return None

    def renderPupila(self, points):
        P1 = (points["Center"]["x"] - points["Radio"]["Value"], points["Center"]["y"] - points["Radio"]["Value"])
        P2 = (points["Center"]["x"] + points["Radio"]["Value"], points["Center"]["y"] + points["Radio"]["Value"])
        self.draw.ellipse((P1, P2), fill=(255, 255, 255), outline=(255, 255, 255))

    # self.draw.ellipse((P1, P2), fill=1)

    def renderLengua(self, points):
        P1 = (points["P1"]["x"], points["P1"]["y"])
        P2 = (points["P2"]["x"], points["P2"]["y"])
        P3 = (points["P3"]["x"], points["P3"]["y"])
        P4 = (points["P4"]["x"], points["P4"]["y"])
        self.draw.polygon(getPointsBezier([P1, P2, P3, P4]), fill=(131,131,255), outline=(0,0,0))

    def renderParpado(self, points):
        P1 = (points["P1"]["x"], points["P1"]["y"])
        P2 = (points["P2"]["x"], points["P2"]["y"])
        P3 = (points["P3"]["x"], points["P3"]["y"])
        P4 = (points["P4"]["x"], points["P4"]["y"])
        self.draw.polygon(getPointsBezier([P1, P2, P3]) + getPointsBezier([P3, P4, P1]), fill=(255, 255, 255))

    def renderMejilla(self, points):
        P1 = (points["P1"]["x"], points["P1"]["y"])
        P2 = (points["P2"]["x"], points["P2"]["y"])
        P3 = (points["P3"]["x"], points["P3"]["y"])
        P4 = (points["P4"]["x"], points["P4"]["y"])
        self.draw.polygon(getPointsBezier([P1, P2, P3]) + getPointsBezier([P3, P4, P1]), fill=(255, 255, 255))

    def renderCeja(self, points):
        P1 = (points["P1"]["x"], points["P1"]["y"])
        P2 = (points["P2"]["x"], points["P2"]["y"])
        P3 = (points["P3"]["x"], points["P3"]["y"])
        P4 = (points["P4"]["x"], points["P4"]["y"])
        self.draw.polygon(getPointsBezier([P1, P2, P3]) + getPointsBezier([P3, P4, P1]), fill=1)

    def renderOjo(self, points):
        P1 = (points["Center"]["x"] - points["Radio1"]["Value"], points["Center"]["y"] - points["Radio2"]["Value"])
        P2 = (points["Center"]["x"] + points["Radio1"]["Value"], points["Center"]["y"] + points["Radio2"]["Value"])
        # P1 = (points["P1"]["x"], points["P1"]["y"])
        # P2 = (points["P2"]["x"], points["P2"]["y"])
        self.draw.ellipse((P1, P2), fill=1)

    def renderBoca(self, points):
        P1 = (points["P1"]["x"], points["P1"]["y"])
        P2 = (points["P2"]["x"], points["P2"]["y"])
        P3 = (points["P3"]["x"], points["P3"]["y"])
        P4 = (points["P4"]["x"], points["P4"]["y"])
        P5 = (points["P5"]["x"], points["P5"]["y"])
        P6 = (points["P6"]["x"], points["P6"]["y"])
        self.draw.polygon(getPointsBezier([P1, P2, P3]) + getPointsBezier([P4, P5, P6]), fill=1, outline=10)

    def setConfig(self, config):
        # with self.mutex:
        self.config_target = config
        self.old_config = self.config
        self.t = 0.06666666666666667
        # self.start()


ic = None

NoneEmotion = -1
Fear = 0
Surprise = 1
Anger = 2
Sadness = 3
Disgust = 4
Joy = 5
Neutral = 7


class Client(Ice.Application, threading.Thread):

    def __init__(self, argv):
        threading.Thread.__init__(self)

        self.adv = 0
        self.rot = 0
        self.max_rot = 0.4
        self.image = np.zeros((240, 320, 3), np.uint8)
        self.usList = [1000] * 7
        self.lasers_proxys = []
        self.angleCamera = 0
        self.emotion_current_exist = False
        self.currentEmotion = NoneEmotion
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
                    print("Connection Successful: ", proxyString)
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
                    print("Connection Successful: ", proxyString)
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
                    print("Connection Successful: ", proxyString)
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
                    while (True):
                        try:
                            i += 1
                            basePrx = ic.stringToProxy(proxyString)
                            self.emotionrecognition_proxy = RoboCompEmotionRecognition.EmotionRecognitionPrx.checkedCast(
                                basePrx)
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
        self.configEmotions = {}
        self.readSonars()
        self.face = Face(self.display_proxy)

        for path in os.listdir(os.path.join(imgPaths, "emotionConfig")):
            if os.path.splitext(path)[1] == ".json":
                with open(os.path.join(imgPaths, "emotionConfig", path), "r") as f:
                    self.configEmotions[os.path.splitext(path)[0]] = json.loads(f.read())
        self.active = True
        self.start()
        self.face.start()

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
            # path = self.face.render()
            # if path != None:
            #     self.display_proxy.setImageFromFile(path)
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

    # def setRobotSpeed(self, vAdvance=0, vRotation=0):
    #     try:
    #         self.adv = vAdvance
    #         self.rot = vRotation
    #         self.differentialrobot_proxy.setSpeedBase(-self.adv*8, self.rot*15)
    #     except Exception as e:
    #         print("Error setRobotSpeed")

    def setRobotSpeed(self, vAdvance=0, vRotation=0):
        # if vAdvance!=0 or vRotation!=0:
        self.adv = vAdvance
        self.rot = vRotation
        self.differentialrobot_proxy.setSpeedBase(self.adv, self.rot)

    def expressFear(self):
        if self.currentEmotion is not Fear:
            self.face.setConfig(self.configEmotions["Fear"])
            self.currentEmotion = Fear
            # self.display_proxy.setImageFromFile(
            #     os.path.join(imgPaths, "miedo.png"))

    # def sendImage(self):
    #     path = self.face.render()
    #     while path != None:
    #         self.display_proxy.setImageFromFile(path)
    #         path = self.face.render()

    def expressSurprise(self):
        if self.currentEmotion is not Surprise:
            self.face.setConfig(self.configEmotions["Surprise"])
            self.currentEmotion = Surprise
        # with open("/home/ivan/Expresiones/sorpresa.json", "r") as f:
        #     config = json.loads(f.read())
        #     self.face.setConfig(config)
        # self.sendImage()
        # self.display_proxy.setImageFromFile(
        #     os.path.join(imgPaths,"sorpresa.png"))

    def expressAnger(self):
        if self.currentEmotion is not Anger:
            self.face.setConfig(self.configEmotions["Anger"])
            self.currentEmotion = Anger
        #
        # with open("/home/ivan/Expresiones/Enfado.json", "r") as f:
        #     config = json.loads(f.read())
        #     self.face.setConfig(config)
        # self.sendImage()
        # self.display_proxy.setImageFromFile(
        #     os.path.join(imgPaths,"ira.png"))

    def expressSadness(self):
        if self.currentEmotion is not Sadness:
            self.face.setConfig(self.configEmotions["Sadness"])
            self.currentEmotion = Sadness
        # with open("/home/ivan/Expresiones/Triste.json", "r") as f:
        #     config = json.loads(f.read())
        #     self.face.setConfig(config)
        #
        # self.sendImage()
        # self.display_proxy.setImageFromFile(
        #     os.path.join(imgPaths,"tristeza.png"))

    def expressDisgust(self):
        if self.currentEmotion is not Disgust:
            self.face.setConfig(self.configEmotions["Disgust"])
            self.currentEmotion = Disgust
        # self.display_proxy.setImageFromFile(
        #     os.path.join(imgPaths, "asco.png"))

    def expressJoy(self):
        if self.currentEmotion is not Joy:
            self.face.setConfig(self.configEmotions["Joy"])
            self.currentEmotion = Joy

        # print("expressJoy")
        # with open("/home/ivan/Expresiones/alegria.json", "r") as f:
        #     config = json.loads(f.read())
        #     self.face.setConfig(config)
        #
        # self.sendImage()
        # self.display_proxy.setImageFromFile(
        #     os.path.join(imgPaths,"alegria.png"))

    def expressNeutral(self):
        if self.currentEmotion is not Neutral:
            self.face.setConfig(self.configEmotions["Neutral"])
            self.currentEmotion = Neutral
        # with open("/home/ivan/Expresiones/neutral.json", "r") as f:
        #     config = json.loads(f.read())
        #     self.face.setConfig(config)
        #
        # self.sendImage()
        # self.display_proxy.setImageFromFile(
        #     os.path.join(imgPaths,"SinEmocion2.png"))

    def setJointAngle(self, angle):
        self.angleCamera = angle
        goal = RoboCompJointMotor.MotorGoalPosition()
        goal.name = 'servo'
        goal.position = -angle
        self.jointmotor_proxy.setPosition(goal)

    def getCurrentEmotion(self):
        return self.currentEmotion

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
