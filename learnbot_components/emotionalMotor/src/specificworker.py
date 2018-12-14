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

from PySide import QtGui, QtCore
from learnbot_components.emotionalMotor.src.genericworker import *
from PIL import Image, ImageDraw
# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel
configPath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'etc','config')
DEFAULTCONFIGNEUTRAL = {'cejaD': {'P2': {'y': 73, 'x': 314}, 'P3': {'y': 99, 'x': 355}, 'P1': {'y': 99, 'x': 278}, 'P4': {'y': 94, 'x': 313}}, 'ojoI': {'P2': {'y': 186, 'x': 196}, 'P1': {'y': 117, 'x': 127}}, 'cejaI': {'P2': {'y': 73, 'x': 160}, 'P3': {'y': 99, 'x': 201}, 'P1': {'y': 99, 'x': 122}, 'P4': {'y': 94, 'x': 160}}, 'ojoD': {'P2': {'y': 186, 'x': 351}, 'P1': {'y': 117, 'x': 282}}, 'boca': {'P2': {'y': 231, 'x': 239}, 'P3': {'y': 234, 'x': 309}, 'P1': {'y': 234, 'x': 170}, 'P6': {'y': 242, 'x': 170}, 'P4': {'y': 242, 'x': 309}, 'P5': {'y': 241, 'x': 239}}}
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

class Face():

	def __init__(self):
		self.img = Image.new('RGB', (480, 320), (255, 255, 255))
		self.draw = ImageDraw.Draw(self.img)
		self.config = DEFAULTCONFIGNEUTRAL
		self.old_config = DEFAULTCONFIGNEUTRAL
		self.t = 0.06666666666666667
		self.config_target = None

	def render(self):
		if self.t <= 1 and self.config_target is not None:
			self.config = getBecierConfig(self.old_config, self.config_target, self.t)
			self.draw.rectangle(((0, 0), (479, 319)), fill=(255, 255, 255), outline=(255, 255, 255))
			self.renderOjo(self.config["ojoI"])
			self.renderOjo(self.config["ojoD"])
			self.renderParpado(self.config["parpadoI"])
			self.renderParpado(self.config["parpadoD"])
			self.renderCeja(self.config["cejaI"])
			self.renderCeja(self.config["cejaD"])
			self.renderBoca(self.config["boca"])
			self.renderPupila(self.config["pupilaI"])
			self.renderPupila(self.config["pupilaD"])
			self.renderMejilla(self.config["mejillaI"])
			self.renderMejilla(self.config["mejillaD"])
			self.t += OFFSET
			path = "/dev/fb0"
			with open(path, "wb") as f:
				f.write(self.img.tobytes())

			# np.array(self.img)
			# cv2.imwrite("/tmp/ebofaceimg.png",np.array(self.img))
			return path
		else:
			self.old_config = self.config_target
			self.config_target = None
		return None

	def renderPupila(self, points):
		P1 = (points["Center"]["x"] - points["Radio"]["Value"], points["Center"]["y"] - points["Radio"]["Value"])
		P2 = (points["Center"]["x"] + points["Radio"]["Value"], points["Center"]["y"] + points["Radio"]["Value"])
		self.draw.ellipse((P1, P2), fill=(255,255,255), outline=(255,255,255))
		# self.draw.ellipse((P1, P2), fill=1)

	def renderParpado(self, points):
		P1 = (points["P1"]["x"], points["P1"]["y"])
		P2 = (points["P2"]["x"], points["P2"]["y"])
		P3 = (points["P3"]["x"], points["P3"]["y"])
		P4 = (points["P4"]["x"], points["P4"]["y"])
		self.draw.polygon(getPointsBezier([P1,P2,P3]) + getPointsBezier([P3,P4,P1]), fill=(255,255,255))

	def renderMejilla(self, points):
		P1 = (points["P1"]["x"], points["P1"]["y"])
		P2 = (points["P2"]["x"], points["P2"]["y"])
		P3 = (points["P3"]["x"], points["P3"]["y"])
		P4 = (points["P4"]["x"], points["P4"]["y"])
		self.draw.polygon(getPointsBezier([P1,P2,P3]) + getPointsBezier([P3,P4,P1]), fill=(255,255,255))

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
		self.config_target = config
		self.old_config = self.config
		self.t = 0.06666666666666667


class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 66
		self.timer.start(self.Period)
		self.face = Face()
		self.configEmotions = {}
		for path in os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), "JSON")):
			with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "JSON", path), "r") as f:
				self.configEmotions[os.path.splitext(f)[0]] = json.loads(f.read())

	def setParams(self, params):
		return True

	@QtCore.Slot()
	def compute(self):
		path = self.face.render()
		# if path is not None:
			# self.display_proxy.setImageFromFile(path)
		return True

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
