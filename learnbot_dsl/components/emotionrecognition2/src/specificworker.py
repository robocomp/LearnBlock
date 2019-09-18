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
from __future__ import print_function, absolute_import

import traceback
import numpy as np
import cv2
import tensorflow as tf
import dlib
from tensorflow.python.platform import gfile
from learnbot_dsl.components.emotionrecognition2.src.genericworker import *
from learnbot_dsl.components.emotionrecognition2.src.face_alignment import FaceAligner
import learnbot_dsl.components.emotionrecognition2.src.face_detector as face_detector
import tempfile
from pyunpack import Archive
configPath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'etc','config')

MODEL_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),'assets','emotion_classifier.pb')
IMAGE_SIZE = 128
NUM_CHANNELS = 1
NUM_FL = 272
EMOTIONS=['Happy','Sad','Neutral','Angry','Surprised']
path = os.path.dirname(os.path.dirname(__file__))

# tempfile.tempdir = tempfile.mkdtemp()
# Archive(path+'/assets/shape_predictor_68_face_landmarks.dat.7z.001').extractall(tempfile.gettempdir())
# # if !os.path.isfile(os.path.dirname(__file__))+'/assets/shape_predictor_68_face_landmarks.dat'):

face_cascade = cv2.CascadeClassifier(os.path.join(path,'assets','haarcascade_frontalface_default.xml'))
predictor = dlib.shape_predictor(os.path.join(path,'assets','shape_predictor_68_face_landmarks.dat'))

features = np.empty([1, NUM_FL], dtype=np.float64)
class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map):
        super(SpecificWorker, self).__init__(proxy_map)
        self.timer.timeout.connect(self.compute)
        self.Period = 100
        # self.timer.start(self.Period)

        # Create a tensorflow session
        self.sess=tf.Session()

        # Read the frozen graph from the model file
        with gfile.FastGFile(MODEL_FILE,'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            self.sess.graph.as_default()
            tf.import_graph_def(graph_def, name='')

            # Get input and output tensors from graph
            self.x_input = self.sess.graph.get_tensor_by_name("input:0")
            self.output = self.sess.graph.get_tensor_by_name("output:0")

    def setParams(self, params):
        return True

    @QtCore.Slot()
    def compute(self):
        # print('SpecificWorker.compute...')


        return True

    # def getEmotionList(self):
    #     return self.emotionList


    #
    # processimage
    #
    def processimage(self, frame):
        emotions_temp = list()
        try:
            arr = np.fromstring(frame.image, np.uint8)
            frame = np.reshape(arr, (frame.width, frame.height, frame.depth))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # frame = cv2.flip(frame, 0)
            gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY )
            # Detect faces
            faces = face_detector.detect(frame)
            for (x1,y1,x2,y2) in faces:

                # Align the face
                fa = FaceAligner(predictor,desiredFaceWidth=IMAGE_SIZE*2)
                faceAligned = fa.align(frame, gray, dlib.rectangle(x1,y1,x2,y2))

                # Convert to grayscale
                faceAligned = cv2.cvtColor(faceAligned,cv2.COLOR_RGB2GRAY)

                # Closely crop out the face
                faces2 = face_cascade.detectMultiScale(faceAligned)
                if len(faces2) == 0 :
                    continue
                (x,y,w,h) = faces2[0]
                cropped_frame = faceAligned[y:y+h, x:x+w]

                # Apply adaptive histogram equalization
                clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(2,2))
                cropped_frame = clahe.apply(cropped_frame)

                # Resize the image
                cropped_frame = cv2.resize(cropped_frame, (IMAGE_SIZE,IMAGE_SIZE))

                # Do necessary preprocessing
                cropped_frame = cropped_frame.reshape((1,IMAGE_SIZE,IMAGE_SIZE,NUM_CHANNELS))
                cropped_frame = (cropped_frame-np.mean(cropped_frame))/np.std(cropped_frame)

                # Feed the cropped and preprocessed frame to classifier
                result = self.sess.run(self.output, {self.x_input:cropped_frame})

                # Get the emotion
                emotion = EMOTIONS[np.argmax(result)]

                # Store emotion data
                emotionData = SEmotion()
                emotionData.x = x1
                emotionData.y = y1
                emotionData.w = abs(x2-x1)
                emotionData.h = abs(y2-y1)
                emotionData.emotion = emotion
                emotions_temp.append(emotionData)

                # For testing purpose
                # cv2.imshow("Image Fed to Classifier", cropped_frame.reshape((IMAGE_SIZE, IMAGE_SIZE)))

        except Ice.Exception as e:
            traceback.print_exc()
            print(e)
        finally:
            return emotions_temp
