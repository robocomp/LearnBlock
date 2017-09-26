from __future__ import print_function
import cv2
import numpy as np

LL_red = (0, 70, 50)
LU_red = (10, 255, 255)

LL_blue = (100,50, 50)
LU_blue = (130, 255, 255)


def detect_black_line(frame):
	rgb = cv2.split(frame)
	maxrgb = np.zeros((240,320), np.uint8)
	for channel in rgb:
		maxrgb = cv2.max(maxrgb, channel)

	err, binary = cv2.threshold( maxrgb, 100, 255, cv2.THRESH_BINARY_INV)

	rois = [0,0,0]
	rois[0]=cv2.countNonZero(binary[10:240,0:120])
	rois[1]=cv2.countNonZero(binary[10:240,120:200])
	rois[2]=cv2.countNonZero(binary[10:240,200:320])
	return rois

def detect_red_line(frame):
	hsv=cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
	binary = cv2.inRange(hsv, LL_red, LU_red)

	err, binary = cv2.threshold( binary, 100, 255, cv2.THRESH_BINARY)
	binary = cv2.dilate(binary, None, iterations=3)

	rois = [0,0,0]
	rois[0]=cv2.countNonZero(binary[10:240,0:120])
	rois[1]=cv2.countNonZero(binary[10:240,120:200])
	rois[2]=cv2.countNonZero(binary[10:240,200:320])
	return rois

def detect_blue_line(frame):
	hsv=cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
	binary = cv2.inRange(hsv, LL_blue, LU_blue)

	err, binary = cv2.threshold( binary, 100, 255, cv2.THRESH_BINARY)
	binary = cv2.dilate(binary, None, iterations=3)

	rois = [0,0,0]
	rois[0]=cv2.countNonZero(binary[10:240,0:120])
	rois[1]=cv2.countNonZero(binary[10:240,120:200])
	rois[2]=cv2.countNonZero(binary[10:240,200:320])
	return rois
