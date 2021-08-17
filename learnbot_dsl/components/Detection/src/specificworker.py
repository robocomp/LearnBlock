#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2021 by YOUR NAME HERE
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

from rich.console import Console
from genericworker import *
import numpy as np
import tensorflow as tf
import cv2
import traceback

Ice.loadSlice("-I ./src/ --all ./DetectionComponent.ice")
from RoboCompDetectionComponent import *

sys.path.append('/opt/robocomp/lib')
console = Console(highlight=False)

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel


LABELS = ['person',
          'bicycle',
          'car',
          'motorcycle',
          'airplane',
          'bus',
          'train',
          'truck',
          'boat',
          'traffic light',
          'fire hydrant',
          'street sign',
          'stop sign',
          'parking meter',
          'bench',
          'bird',
          'cat',
          'dog',
          'horse',
          'sheep',
          'cow',
          'elephant',
          'bear',
          'zebra',
          'giraffe',
          'hat',
          'backpack',
          'umbrella',
          'shoe',
          'eye glasses',
          'handbag',
          'tie',
          'suitcase',
          'frisbee',
          'skis',
          'snowboard',
          'sports ball',
          'kite',
          'baseball bat',
          'baseball glove',
          'skateboard',
          'surfboard',
          'tennis racket',
          'bottle',
          'plate',
          'wine glass',
          'cup',
          'fork',
          'knife',
          'spoon',
          'bowl',
          'banana',
          'apple',
          'sandwich',
          'orange',
          'broccoli',
          'carrot',
          'hot dog',
          'pizza',
          'donut',
          'cake',
          'chair',
          'couch',
          'potted plant',
          'bed',
          'mirror',
          'dining table',
          'window',
          'desk',
          'toilet',
          'door',
          'tv',
          'laptop',
          'mouse',
          'remote',
          'keyboard',
          'cell phone',
          'microwave',
          'oven',
          'toaster',
          'sink',
          'refrigerator',
          'blender',
          'book',
          'clock',
          'vase',
          'scissors',
          'teddy bear',
          'hair drier',
          'toothbrush',
          'hair brush']


class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map, startup_check=False):
        super(SpecificWorker, self).__init__(proxy_map)
        self.Period = 2000

        # Set a default threshold
        self.threshold = 0.3

        # Read the model
        self.interpreter: tf.lite.Interpreter = tf.lite.Interpreter("../models/model_efficientdet.tflite")
        self.interpreter.allocate_tensors()

        # Get the input and output tensors
        self.input_details: list = self.interpreter.get_input_details()
        self.output_details: list = self.interpreter.get_output_details()

        if startup_check:
            self.startup_check()
        else:
            pass

    def __del__(self):
        console.print('SpecificWorker destructor')

    def setParams(self, params):
        # try:
        #	self.innermodel = InnerModel(params["InnerModelPath"])
        # except:
        #	traceback.print_exc()
        #	print("Error reading config params")
        return True

    def compute(self):
        print('SpecificWorker.compute...')
        while True: pass
        # computeCODE
        # try:
        #   self.differentialrobot_proxy.setSpeedBase(100, 0)
        # except Ice.Exception as e:
        #   traceback.print_exc()
        #   print(e)

        # The API of python-innermodel is not exactly the same as the C++ version
        # self.innermodel.updateTransformValues('head_rot_tilt_pose', 0, 0, 0, 1.3, 0, 0)
        # z = librobocomp_qmat.QVec(3,0)
        # r = self.innermodel.transform('rgbd', z, 'laser')
        # r.printvector('d')
        # print(r[0], r[1], r[2])

        return True

    def startup_check(self):
        import time
        time.sleep(0.2)
        exit()

    # =============== Methods for Component Implements ==================
    # ===================================================================

    #
    # IMPLEMENTATION of getThreshold method from DetectionComponent interface
    #
    def DetectionComponent_getThreshold(self):
        return self.threshold

    #
    # IMPLEMENTATION of processImage method from DetectionComponent interface
    #
    def DetectionComponent_processImage(self, frame):
        predictions = list()
        try:
            # Convert the bytes of the image to a tensor with shape (width,height,3) RGB
            arr = np.fromstring(frame.image, np.uint8)
            image = np.reshape(arr, (frame.width, frame.height, frame.depth))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Preprocess the image
            image = cv2.resize(image, dsize=(448, 448))
            image = np.expand_dims(image, axis=0)

            # Execute the interpreter
            self.interpreter.set_tensor(self.input_details[0]['index'], image)
            self.interpreter.invoke()

            # Get the outputs of the model
            boxes: np.array = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            classes: np.array = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
            scores: np.array = self.interpreter.get_tensor(self.output_details[2]['index'])[0]
            num_predictions: int = int(self.interpreter.get_tensor(self.output_details[3]['index'])[0])

            # Prepare the data according to the interface
            for i in range(num_predictions):
                if scores[i] > self.threshold:
                    prediction = SPrediction()
                    prediction.x = int(boxes[i][1] * frame.height)
                    prediction.y = int(boxes[i][0] * frame.width)
                    prediction.w = int((boxes[i][3]-boxes[i][1]) * frame.height)
                    prediction.h = int((boxes[i][2]-boxes[i][0]) * frame.width)
                    prediction.label = LABELS[int(classes[i])]
                    predictions.append(prediction)

        except Ice.Exception as e:
            traceback.print_exc()
            print(e)
        finally:
            return predictions

    #
    # IMPLEMENTATION of setThreshold method from DetectionComponent interface
    #
    def DetectionComponent_setThreshold(self, threshold):
        self.threshold = threshold

    # ===================================================================
    # ===================================================================

    ######################
    # From the DetectionComponent you can use this types:
    # DetectionComponent.SPrediction
    # DetectionComponent.TImage
