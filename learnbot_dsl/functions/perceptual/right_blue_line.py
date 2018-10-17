from __future__ import print_function
import cv2
import numpy as np
import visual_auxiliary as va

def right_blue_line(lbot, params=None, verbose=False):
	frame = lbot.getImage()
	rois = va.detect_blue_line(frame)
	if verbose:
		print("Blue points", rois)
	
	maxIndex = np.argmax(rois)
	if maxIndex==2 and rois[maxIndex]>20:
		return True
	return False
