from __future__ import print_function, absolute_import
import sys, os, numpy as np

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import visual_auxiliary as va

def is_center_red_line(lbot):
	frame = lbot.getImage()
	if frame is not None:
		rois = va.detect_red_line(frame)
		maxIndex = np.argmax(rois)
		if maxIndex == 1 and rois[maxIndex] > 20:
			return True
	return False
