from __future__ import print_function, absolute_import
import cv2
import numpy as np
import learnbot_dsl.functions.perceptual.visual_auxiliary as va

def right_blue_line(lbot, params=None, verbose=False):
	frame = lbot.getImage()
	rois = va.detect_blue_line(frame)
	if verbose:
		print("Blue points", rois)
	
	maxIndex = np.argmax(rois)
	if maxIndex==2 and rois[maxIndex]>20:
		return True
	return False
