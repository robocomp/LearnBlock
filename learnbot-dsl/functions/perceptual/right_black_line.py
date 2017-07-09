from __future__ import print_function
import cv2
import numpy as np

def right_black_line(lbot, params=None, verbose=False):
	frame = lbot.getImage()
	rgb = cv2.split(frame)
	maxrgb = np.zeros((240,320), np.uint8)
	for channel in rgb:
		maxrgb = cv2.max(maxrgb, channel)

	err, binary = cv2.threshold( maxrgb, 20, 255, cv2.THRESH_BINARY_INV)

	rois = [0,0,0]
	rois[0]=cv2.countNonZero(binary[160:200,10:110])
	rois[1]=cv2.countNonZero(binary[160:200,110:210])
	rois[2]=cv2.countNonZero(binary[160:200,210:310])

	if verbose:
		print("Black points", rois)
	
	maxIndex = np.argmax(rois)
	if maxIndex==2 and rois[maxIndex]>100:
		return True
	return False
