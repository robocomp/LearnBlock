from __future__ import print_function, absolute_import
import cv2
import numpy as np
import sys, os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import visual_auxiliary as va

def is_there_ground(lbot):
	gsensors = lbot.getGroundSensors()
	return gsensors["left"] and gsensors["right"]
