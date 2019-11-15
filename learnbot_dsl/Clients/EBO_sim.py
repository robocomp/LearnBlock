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

ICEs = ["Laser.ice", "DifferentialRobot.ice", "JointMotor.ice", "Display.ice", "RGBD.ice", "GenericBase.ice"]
icePaths = []
icePaths.append(PATHINTERFACES)
for ice in ICEs:
    for p in icePaths:
        if os.path.isfile(os.path.join(p, ice)):
            wholeStr = ' -I' + p + " --all " + os.path.join(p, ice)
            Ice.loadSlice(wholeStr)
            break

import RoboCompLaser, RoboCompDifferentialRobot, RoboCompJointMotor, RoboCompGenericBase, RoboCompDisplay, RoboCompRGBD

DEFAULTCONFIGNEUTRAL = {
    "cejaD": {"P2": {"y": 73, "x": 314},
                                  "P3": {"y": 99, "x": 355},
                                  "P1": {"y": 99, "x": 278},
                                  "P4": {"y": 94, "x": 313}
                                  },
                        "parpadoI": {"P2": {"y": 80, "x": 160},
                                     "P3": {"y": 151, "x": 214},
                                     "P1": {"y": 151, "x": 112},
                                     "P4": {"y": 80, "x": 160}},
                        "ojoI": {"Radio1": {"Value": 34},
                                 "Center": {"y": 151, "x": 161},
                                 "Radio2": {"Value": 34}},
                        "cejaI": {"P2": {"y": 73, "x": 160},
                                  "P3": {"y": 99, "x": 201},
                                  "P1": {"y": 99, "x": 122},
                                  "P4": {"y": 94, "x": 160}},
                        "ojoD": {"Radio1": {"Value": 34},
                                 "Center": {"y": 151, "x": 316},
                                 "Radio2": {"Value": 34}},
                        "boca": {"P2": {"y": 231, "x": 239},
                                 "P3": {"y": 234, "x": 309},
                                 "P1": {"y": 234, "x": 170},
                                 "P6": {"y": 242, "x": 170},
                                 "P4": {"y": 242, "x": 309},
                                 "P5": {"y": 241, "x": 239}},
                        "pupilaD": {"Radio": {"Value": 5},
                                    "Center": {"y": 151, "x": 316}},
                        "lengua": {"P2": {"y": 238, "x": 239},
                                   "P3": {"y": 238, "x": 309},
                                   "P1": {"y": 238, "x": 199},
                                   "P4": {"y": 238, "x": 273}},
                        "mejillaI": {"P2": {"y": 188, "x": 160},
                                     "P3": {"y": 187, "x": 201},
                                     "P1": {"y": 187, "x": 122},
                                     "P4": {"y": 187, "x": 160}},
                        "parpadoD": {"P2": {"y": 80, "x": 314},
                                     "P3": {"y": 151, "x": 369},
                                     "P1": {"y": 151, "x": 266},
                                     "P4": {"y": 80, "x": 313}},
                        "pupilaI": {"Radio": {"Value": 5},
                                    "Center": {"y": 151, "x": 161}},
                        "mejillaD": {"P2": {"y": 188, "x": 314},
                                     "P3": {"y": 187, "x": 355},
                                     "P1": {"y": 187, "x": 278},
                                     "P4": {"y": 187, "x": 313}}}

OFFSET = 0.06666666666666667

imgPaths = os.path.join(Learnblock_Path, 'imgs')

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
            if point in ["Radio", "Radio1", "Radio2"]:
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
        self.stopped = False

    def run(self):
        start = time.time()
        sec = randint(2,6)
        while not self.stopped:
            time.sleep(0)
            #print(time.time() - start, sec)
            if time.time() - start > sec:
                self.pestaneo()
                sec = randint(2, 6)
                start = time.time()
                # print("entro")
            path = self.render()
            if path is not None:
                self.display_proxy.setImageFromFile(path)

    def pestaneo(self):
        configaux = copy.copy(self.config)
        value1 = copy.copy((configaux["ojoD"]["Radio2"]["Value"]))
        value2 = copy.copy((configaux["ojoI"]["Radio2"]["Value"]))

        for t in [(x+1)/5. for x in range(5)] + sorted([(x)/5. for x in range(5)], reverse=True):
            configaux["ojoD"]["Radio2"]["Value"] = bezier((value1,0), (0,0), t)[0]
            configaux["ojoI"]["Radio2"]["Value"] = bezier((value2, 0), (0, 0), t)[0]
            # config1 = getBecierConfig(configaux, configPestaneo, t)
            self.drawConfig(configaux)
            img = np.array(self.img)
            img = cv2.flip(img, 1)
            cv2.imwrite("/tmp/ebofaceimg.png", img)
            self.display_proxy.setImageFromFile("/tmp/ebofaceimg.png")
            # time.sleep(0.01)


    def drawConfig(self, config):
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

    def render(self):
        if self.t <= 1 and self.config_target is not None:
            config = self.config = getBecierConfig(self.old_config, self.config_target, self.t)
            self.t += OFFSET
            self.drawConfig(config)
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

    def stop(self):
        self.stopped = True
        self.join()

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
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "EBO_sim.cfg"), "rb") as f:
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
        self.display_proxy = connectComponent("display:tcp -h " + robotIP + " -p 30000",
                                                     RoboCompDisplay.DisplayPrx)
        self.rgbd_proxy = connectComponent("rgbd:tcp -h " + robotIP + " -p 10097", RoboCompRGBD.RGBDPrx)

        self.configEmotions = {}
        self.face = Face(self.display_proxy)

        for path in os.listdir(os.path.join(imgPaths, "emotionConfig")):
            if os.path.splitext(path)[1] == ".json":
                with open(os.path.join(imgPaths, "emotionConfig", path), "r") as f:
                    self.configEmotions[os.path.splitext(path)[0]] = json.loads(f.read())
        self.face.start()

    def disconnect(self):
        self.deviceMove(0, 0)
        self.face.stop()

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
            self.face.setConfig(self.configEmotions["Joy"])
        elif _emotion is Emotions.Sadness:
            self.face.setConfig(self.configEmotions["Sadness"])
        elif _emotion is Emotions.Surprise:
            self.face.setConfig(self.configEmotions["Surprise"])
        elif _emotion is Emotions.Disgust:
            self.face.setConfig(self.configEmotions["Disgust"])
        elif _emotion is Emotions.Anger:
            self.face.setConfig(self.configEmotions["Anger"])
        elif _emotion is Emotions.Fear:
            self.face.setConfig(self.configEmotions["Fear"])
        elif _emotion is Emotions.Neutral:
            self.face.setConfig(self.configEmotions["Neutral"])

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
