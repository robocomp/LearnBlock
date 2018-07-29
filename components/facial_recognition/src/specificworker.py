#
# Copyright (C) 2018 by YOUR NAME HERE
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

import sys
import os
import traceback
import time

import cv2
import numpy as np

from statistics import mode
from PySide import QtGui, QtCore
from genericworker import *
from keras.models import load_model

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input
from threading import Lock


# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 0
		self.timer.start(self.Period)

		self.detection_model_path = 'src/face_classification/trained_models/detection_models/haarcascade_frontalface_default.xml'
		# self.detection_model_path2 = 'src/face_classification/trained_models/detection_models/haarcascade_profileface.xml'
		self.emotion_model_path = 'src/face_classification/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
		self.emotion_labels = get_labels('fer2013')
		self.frame_window = 10
		self.emotion_offsets = (20, 40)
		self.face_detection = load_detection_model(self.detection_model_path)
		# self.face_detection2 = load_detection_model(self.detection_model_path2)
		self.emotion_classifier = load_model(self.emotion_model_path, compile=False)
		self.emotion_target_size = self.emotion_classifier.input_shape[1:3]
		self.emotion_window = []
		# cv2.namedWindow('window_frame')
		self.video_capture = cv2.VideoCapture(0)
		self.list_emotions = []

	def setParams(self, params):
		#try:
		#	self.innermodel = InnerModel(params["InnerModelPath"])
		#except:
		#	traceback.print_exc()
		#	print "Error reading config params"
		return True

	@QtCore.Slot()
	def compute(self):

		bgr_image = self.video_capture.read()[1]
		gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
		rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
		faces = detect_faces(self.face_detection, gray_image)
		# faces2 = detect_faces(self.face_detection2, gray_image)
		# for faces in [faces1,faces2]:
		self.mutex.lock()
		self.list_emotions = []
		for face_coordinates in faces:

			x1, x2, y1, y2 = apply_offsets(face_coordinates, self.emotion_offsets)
			gray_face = gray_image[y1:y2, x1:x2]
			try:
				gray_face = cv2.resize(gray_face, (self.emotion_target_size))
			except:
				continue

			gray_face = preprocess_input(gray_face, True)
			gray_face = np.expand_dims(gray_face, 0)
			gray_face = np.expand_dims(gray_face, -1)
			emotion_prediction = self.emotion_classifier.predict(gray_face)
			emotion_probability = np.max(emotion_prediction)
			emotion_label_arg = np.argmax(emotion_prediction)
			emotion_text = self.emotion_labels[emotion_label_arg]
			self.emotion_window.append(emotion_text)

			if len(self.emotion_window) > self.frame_window:
				self.emotion_window.pop(0)
			try:
				emotion_mode = mode(self.emotion_window)
			except:
				continue

			if emotion_text == 'angry':
				color = emotion_probability * np.asarray((255, 0, 0))
			elif emotion_text == 'sad':
				color = emotion_probability * np.asarray((0, 0, 255))
			elif emotion_text == 'happy':
				color = emotion_probability * np.asarray((255, 255, 0))
			elif emotion_text == 'surprise':
				color = emotion_probability * np.asarray((0, 255, 255))
			else:
				color = emotion_probability * np.asarray((0, 255, 0))

			# color = color.astype(int)
			# color = color.tolist()

			# draw_bounding_box(face_coordinates, rgb_image, color)
			# draw_text(face_coordinates, rgb_image, emotion_mode,
			# 		  color, 0, -45, 1, 1)
			data = SEmotion()
			data.x, data.y, data.w, data.h = face_coordinates
			data.emotion = emotion_mode
			# self.list_emotions.append((face_coordinates, emotion_mode))
			self.list_emotions.append(data)

		self.mutex.unlock()
		# bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
		# cv2.imshow('window_frame', bgr_image)
		return True


	#
	# getEmotionList

	def getEmotionList(self):

		# implementCODE
		self.mutex.lock()
		emotionL = self.list_emotions
		self.mutex.unlock()
		print emotionL
		return emotionL

