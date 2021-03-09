#
# Copyright (C) 2017 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, os, traceback, time, copy, json
from random import randint

from PySide2 import QtGui, QtCore
from genericworker import *
import numpy as np
import cv2
import threading
# from learnbot_components.emotionalMotor.src.genericworker import *
from PIL import Image, ImageDraw
# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel
configPath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'etc','config')
DEFAULTCONFIGNEUTRAL = {"cejaD": {"P2": {"y": 73, "x": 314}, "P3": {"y": 99, "x": 355}, "P1": {"y": 99, "x": 278}, "P4": {"y": 94, "x": 313}}, "parpadoI": {"P2": {"y": 80, "x": 160}, "P3": {"y": 151, "x": 214}, "P1": {"y": 151, "x": 112}, "P4": {"y": 80, "x": 160}}, "ojoI": {"Radio1": {"Value": 34}, "Center": {"y": 151, "x": 161}, "Radio2": {"Value": 34}}, "cejaI": {"P2": {"y": 73, "x": 160}, "P3": {"y": 99, "x": 201}, "P1": {"y": 99, "x": 122}, "P4": {"y": 94, "x": 160}}, "ojoD": {"Radio1": {"Value": 34}, "Center": {"y": 151, "x": 316}, "Radio2": {"Value": 34}}, "boca": {"P2": {"y": 231, "x": 239}, "P3": {"y": 234, "x": 309}, "P1": {"y": 234, "x": 170}, "P6": {"y": 242, "x": 170}, "P4": {"y": 242, "x": 309}, "P5": {"y": 241, "x": 239}}, "pupilaD": {"Radio": {"Value": 5}, "Center": {"y": 151, "x": 316}}, "lengua": {"P2": {"y": 238, "x": 239}, "P3": {"y": 238, "x": 309}, "P1": {"y": 238, "x": 199}, "P4": {"y": 238, "x": 273}}, "mejillaI": {"P2": {"y": 188, "x": 160}, "P3": {"y": 187, "x": 201}, "P1": {"y": 187, "x": 122}, "P4": {"y": 187, "x": 160}}, "parpadoD": {"P2": {"y": 80, "x": 314}, "P3": {"y": 151, "x": 369}, "P1": {"y": 151, "x": 266}, "P4": {"y": 80, "x": 313}}, "pupilaI": {"Radio": {"Value": 5}, "Center": {"y": 151, "x": 161}}, "mejillaD": {"P2": {"y": 188, "x": 314}, "P3": {"y": 187, "x": 355}, "P1": {"y": 187, "x": 278}, "P4": {"y": 187, "x": 313}}}

OFFSET = 0.06666666666666667
def bezier(p1, p2, t):
	diff = (p2[0] - p1[0], p2[1] - p1[1])
	return [p1[0] + diff[0] * t, p1[1] + diff[1] * t]

def getPointsBezier(points):
	bezierPoints = list()
	pointsCopy = copy.copy(points)
	for t in [x/50. for x in range(51)]:
		while len(points)!=1:
			newPoints = list()
			p1=points[0]
			for p2 in points[1:]:
				newPoints.append(bezier(p1,p2,t))
				p1=p2
			points=newPoints
		bezierPoints.append(tuple(points[0]))
		points=pointsCopy
	return bezierPoints

def getBecierConfig(old_config, config_target, t):
	config = copy.copy(old_config)
	for parte in old_config:
		for point in old_config[parte]:
			if "Radio" in point:
				radio = bezier((old_config[parte][point]["Value"],0), (config_target[parte][point]["Value"],0),t)
				config[parte][point]["Value"] = radio[0]
			else:
				p = bezier((old_config[parte][point]["x"], old_config[parte][point]["y"]), (config_target[parte][point]["x"], config_target[parte][point]["y"]), t)
				config[parte][point]["x"] = p[0]
				config[parte][point]["y"] = p[1]
	return config

#def getBecierConfig(old_config, config_target, t):
#	config = copy.copy(old_config)
#	for parte in old_config:
#		for point in old_config[parte]:
#			p = bezier((old_config[parte][point]["x"], old_config[parte][point]["y"]), (config_target[parte][point]["x"], config_target[parte][point]["y"]), t)
#			config[parte][point]["x"] = p[0]
#			config[parte][point]["y"] = p[1]
#	return config

# class Face():

# 	def __init__(self):
# 		self.img = Image.new('RGBA', (480, 320), (255, 255, 255))
# 		self.draw = ImageDraw.Draw(self.img)
# 		self.config = DEFAULTCONFIGNEUTRAL
# 		self.old_config = DEFAULTCONFIGNEUTRAL
# 		self.t = 0.06666666666666667
# 		self.config_target = None

# 	def drawConfig(self, config):
# 		self.draw.rectangle(((0, 0), (479, 319)), fill=(255, 255, 255), outline=(255, 255, 255))
# 		self.renderOjo(config["ojoI"])
# 		self.renderOjo(config["ojoD"])
# 		self.renderParpado(config["parpadoI"])
# 		self.renderParpado(config["parpadoD"])
# 		self.renderCeja(config["cejaI"])
# 		self.renderCeja(config["cejaD"])
# 		self.renderBoca(config["boca"])
# 		self.renderPupila(config["pupilaI"])
# 		self.renderPupila(config["pupilaD"])
# 		self.renderMejilla(config["mejillaI"])
# 		self.renderMejilla(config["mejillaD"])
# 		self.renderLengua(config["lengua"])

# 	def pestaneo(self):
# 		configaux = copy.copy(self.config)
# 		value1 = copy.copy((configaux["ojoD"]["Radio2"]["Value"]))
# 		value2 = copy.copy((configaux["ojoI"]["Radio2"]["Value"]))
# 		for t in [(x+1)/5. for x in range(5)] + sorted([(x)/5. for x in range(5)], reverse=True):
# 			configaux["ojoD"]["Radio2"]["Value"] = bezier((value1,0), (0,0), t)[0]
# 			configaux["ojoI"]["Radio2"]["Value"] = bezier((value2, 0), (0, 0), t)[0]
# 			# config1 = getBecierConfig(configaux, configPestaneo, t)
# 			self.drawConfig(configaux)
# 			# path = "/dev/fb0"
# 			# with open(path, "wb") as f:
# 			# 	f.write(self.img.tobytes())
# 			# img = np.array(self.img)
# 			# img = cv2.flip(img, 1)
# 			# cv2.imwrite("/tmp/ebofaceimg.png", img)
# 			# self.display_proxy.setImageFromFile("/tmp/ebofaceimg.png")
#             # time.sleep(0.01)

# 	def render(self):
# 		if self.t <= 1 and self.config_target is not None:
# 			self.config = getBecierConfig(self.old_config, self.config_target, self.t)
# 			self.drawConfig(self.config)
# 			# self.draw.rectangle(((0, 0), (479, 319)), fill=(255, 255, 255), outline=(255, 255, 255))
# 			# self.renderOjo(self.config["ojoI"])
# 			# self.renderOjo(self.config["ojoD"])
# 			# self.renderParpado(self.config["parpadoI"])
# 			# self.renderParpado(self.config["parpadoD"])
# 			# self.renderCeja(self.config["cejaI"])
# 			# self.renderCeja(self.config["cejaD"])
# 			# self.renderBoca(self.config["boca"])
# 			# self.renderPupila(self.config["pupilaI"])
# 			# self.renderPupila(self.config["pupilaD"])
# 			# self.renderMejilla(self.config["mejillaI"])
# 			# self.renderMejilla(self.config["mejillaD"])
# 			# self.renderLengua(self.config["lengua"])
# 			self.t += OFFSET
# 			# path = "/dev/fb0"
# 			# with open(path, "wb") as f:
# 			# 	f.write(self.img.tobytes())

# 			path = "/tmp/ebofaceimg.png"
# 			np.array(self.img)
# 			cv2.imwrite(path,np.array(self.img))

# 			return path
# 		else:
# 			self.old_config = self.config_target
# 			self.config_target = None
# 		return None

# 	def renderLengua(self, points):
# 		P1 = (points["P1"]["x"], points["P1"]["y"])
# 		P2 = (points["P2"]["x"], points["P2"]["y"])
# 		P3 = (points["P3"]["x"], points["P3"]["y"])
# 		P4 = (points["P4"]["x"], points["P4"]["y"])
# 		self.draw.polygon(getPointsBezier([P1, P2, P3, P4]), fill=(131,131,255), outline=(0,0,0))

# 	def renderPupila(self, points):
# 		P1 = (points["Center"]["x"] - points["Radio"]["Value"], points["Center"]["y"] - points["Radio"]["Value"])
# 		P2 = (points["Center"]["x"] + points["Radio"]["Value"], points["Center"]["y"] + points["Radio"]["Value"])
# 		self.draw.ellipse((P1, P2), fill=(255,255,255), outline=(255,255,255))
# 		# self.draw.ellipse((P1, P2), fill=1)

# 	def renderParpado(self, points):
# 		P1 = (points["P1"]["x"], points["P1"]["y"])
# 		P2 = (points["P2"]["x"], points["P2"]["y"])
# 		P3 = (points["P3"]["x"], points["P3"]["y"])
# 		P4 = (points["P4"]["x"], points["P4"]["y"])
# 		self.draw.polygon(getPointsBezier([P1,P2,P3]) + getPointsBezier([P3,P4,P1]), fill=(255,255,255))

# 	def renderMejilla(self, points):
# 		P1 = (points["P1"]["x"], points["P1"]["y"])
# 		P2 = (points["P2"]["x"], points["P2"]["y"])
# 		P3 = (points["P3"]["x"], points["P3"]["y"])
# 		P4 = (points["P4"]["x"], points["P4"]["y"])
# 		self.draw.polygon(getPointsBezier([P1,P2,P3]) + getPointsBezier([P3,P4,P1]), fill=(255,255,255))

# 	def renderCeja(self, points):
# 		P1 = (points["P1"]["x"], points["P1"]["y"])
# 		P2 = (points["P2"]["x"], points["P2"]["y"])
# 		P3 = (points["P3"]["x"], points["P3"]["y"])
# 		P4 = (points["P4"]["x"], points["P4"]["y"])
# 		self.draw.polygon(getPointsBezier([P1, P2, P3]) + getPointsBezier([P3, P4, P1]), fill=1)

# 	def renderOjo(self, points):
# 		P1 = (points["Center"]["x"] - points["Radio1"]["Value"], points["Center"]["y"] - points["Radio2"]["Value"])
# 		P2 = (points["Center"]["x"] + points["Radio1"]["Value"], points["Center"]["y"] + points["Radio2"]["Value"])
# 		# P1 = (points["P1"]["x"], points["P1"]["y"])
# 		# P2 = (points["P2"]["x"], points["P2"]["y"])
# 		self.draw.ellipse((P1, P2), fill=1)

# 	def renderBoca(self, points):
# 		P1 = (points["P1"]["x"], points["P1"]["y"])
# 		P2 = (points["P2"]["x"], points["P2"]["y"])
# 		P3 = (points["P3"]["x"], points["P3"]["y"])
# 		P4 = (points["P4"]["x"], points["P4"]["y"])
# 		P5 = (points["P5"]["x"], points["P5"]["y"])
# 		P6 = (points["P6"]["x"], points["P6"]["y"])
# 		self.draw.polygon(getPointsBezier([P1, P2, P3]) + getPointsBezier([P4, P5, P6]), fill=1, outline=10)

# 	def setConfig(self, config):
# 		self.config_target = config
# 		self.old_config = self.config
# 		self.t = 0.06666666666666667

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
            pestaneoFlag = False
            #print(time.time() - start, sec)
            if time.time() - start > sec:
                #self.pestaneo()
                pestaneoFlag = True
                sec = randint(2, 6)
                start = time.time()
                # print("entro")
            self.moveFace(pestaneoFlag, True)
            path = self.render()
            if path is not None:
                self.display_proxy.setImageFromFile(path)

    def moveFace(self, pestaneoFlag, moveMouthFlag):
        if not pestaneoFlag and not moveMouthFlag:
            return

        configaux = copy.copy(self.config)

        # PESTAÑEO
        value1 = copy.copy((configaux["ojoD"]["Radio2"]["Value"]))
        value2 = copy.copy((configaux["ojoI"]["Radio2"]["Value"]))

        # BOCA
        value2x = copy.copy((configaux["boca"]["P2"]["x"]))
        value2y = copy.copy((configaux["boca"]["P2"]["y"]))

        value5x = copy.copy((configaux["boca"]["P5"]["x"]))
        value5y = copy.copy((configaux["boca"]["P5"]["y"]))

        for t in [(x+1)/5. for x in range(5)] + sorted([(x)/5. for x in range(5)], reverse=True):

            if pestaneoFlag:
                configaux["ojoD"]["Radio2"]["Value"] = bezier((value1,0), (0,0), t)[0]
                configaux["ojoI"]["Radio2"]["Value"] = bezier((value2, 0), (0, 0), t)[0]

            if moveMouthFlag:
                configaux["boca"]["P2"]["y"] = bezier((value2x, value2y), (value2x, value2y - 15), t)[1]         
                configaux["boca"]["P5"]["y"] = bezier((value5x, value5y), (value5x, value5y + 15), t)[1]                       
            # config1 = getBecierConfig(configaux, configPestaneo, t)
            self.drawConfig(configaux)
            img = np.array(self.img)
            img = cv2.flip(img, 1)
            cv2.imwrite("/tmp/ebofaceimg.png", img)
            self.display_proxy.setImageFromFile("/tmp/ebofaceimg.png")


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
        #     self.config_target = None
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


class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 10
		self.timer.start(self.Period)
		self.face = Face(self.display_proxy)
		self.start_time = time.time()
		self.sec = randint(2,6)
		self.configEmotions = {}
		json_path = os.path.join(os.path.dirname(__file__),'../JSON')
		for path in os.listdir(json_path):
			with open(os.path.join(json_path, path), "r") as f:
				self.configEmotions[os.path.splitext(path)[0]] = json.loads(f.read())
		self.face.start()

	def setParams(self, params):
		#try:
		#	self.innermodel = InnerModel(params["InnerModelPath"])
		#except:
		#	traceback.print_exc()
		#	print("Error reading config params")
		return True

	@QtCore.Slot()
	def compute(self):
		pass
		# if time.time()- self.start_time > self.sec:
		# 	self.face.pestaneo()
		# 	self.start_time = time.time()
		# 	self.sec = randint(2,6)
		# 	print("compute")
		# path = self.face.render()
		# print(path)
		# if path is not None:
		# 	self.display_proxy.setImageFromFile(path)
		# return True

	def sendImage(self, file):
		img = QtGui.QImage(file)
		self.i+=1
		im = Image()
		im.Img=img.bits()
		im.width=img.width()
		im.height=img.height()
		try:
			self.display_proxy.setImage(im)
		except Exception as e:
			print(e)

	#
	# expressFear
	#
	def expressFear(self):
		self.face.setConfig(self.configEmotions["Fear"])
		# self.display_proxy.setImageFromFile("/home/robocomp/learnbot/learnbot_components/emotionalMotor/imgs/frameBuffer/miedo.fb")

	#
	# expressSurprise
	#
	def expressSurprise(self):
		self.face.setConfig(self.configEmotions["Surprise"])
		# self.display_proxy.setImageFromFile("/home/robocomp/learnbot/learnbot_components/emotionalMotor/imgs/frameBuffer/sorpresa.fb")

	#
	# expressAnger
	#
	def expressAnger(self):
		self.face.setConfig(self.configEmotions["Anger"])
		# self.display_proxy.setImageFromFile("/home/robocomp/learnbot/learnbot_components/emotionalMotor/imgs/frameBuffer/ira.fb")

	#
	# expressSadness
	#
	def expressSadness(self):
		self.face.setConfig(self.configEmotions["Sadness"])
		# self.display_proxy.setImageFromFile("/home/robocomp/learnbot/learnbot_components/emotionalMotor/imgs/frameBuffer/tristeza.fb")

	#
	# expressDisgust
	#
	def expressDisgust(self):
		self.face.setConfig(self.configEmotions["Disgust"])
		# self.display_proxy.setImageFromFile("/home/robocomp/learnbot/learnbot_components/emotionalMotor/imgs/frameBuffer/asco.fb")

	#
	# expressJoy
	#
	def expressJoy(self):
		self.face.setConfig(self.configEmotions["Joy"])
		# self.display_proxy.setImageFromFile("/home/robocomp/learnbot/learnbot_components/emotionalMotor/imgs/frameBuffer/alegria.fb")

	#
	# expressNeutral
	#
	def expressNeutral(self):
		self.face.setConfig(self.configEmotions["Neutral"])
		# self.display_proxy.setImageFromFile("/home/robocomp/learnbot/learnbot_components/emotionalMotor/imgs/frameBuffer/SinEmocion2.fb")

