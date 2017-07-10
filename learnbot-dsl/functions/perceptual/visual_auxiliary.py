from __future__ import print_function
import cv2
import numpy as np

def detect_black_line(frame):
	rgb = cv2.split(frame)
	maxrgb = np.zeros((240,320), np.uint8)
	for channel in rgb:
		maxrgb = cv2.max(maxrgb, channel)

	err, binary = cv2.threshold( maxrgb, 20, 255, cv2.THRESH_BINARY_INV)

	rois = [0,0,0]
	rois[0]=cv2.countNonZero(binary[10:240,0:120])
	rois[1]=cv2.countNonZero(binary[10:240,120:200])
	rois[2]=cv2.countNonZero(binary[10:240,200:320])
	return rois
