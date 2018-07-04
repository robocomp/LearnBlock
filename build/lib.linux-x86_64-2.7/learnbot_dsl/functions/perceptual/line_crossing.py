from __future__ import print_function
import cv2
import numpy as np
import visual_auxiliary as va

def line_crossing(lbot, params=None, verbose=False):
	frame = lbot.getImage()
	roisR = va.detect_red_line(frame)
	roisB = va.detect_black_line(frame)
	if verbose:
		print("Red points", roisR)
		print("Black points", roisB)
	
	if roisR[1]>40 and roisB[1]>40:
		lbot.publish_topic("line_crossing")
		return True
	return False
