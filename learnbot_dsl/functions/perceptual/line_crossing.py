from __future__ import print_function, absolute_import
import cv2
import numpy as np
import learnbot_dsl.functions.perceptual.visual_auxiliary as va

def line_crossing(lbot, params=None, verbose=False):
	frame = lbot.getImage()
	roisR = va.detect_red_line(frame)
	roisB = va.detect_black_line(frame)
	if verbose:
		print("Red points", roisR)
		print("Black points", roisB)
	
	if roisR[1]>40 and roisB[1]>40:
		return True
	return False
