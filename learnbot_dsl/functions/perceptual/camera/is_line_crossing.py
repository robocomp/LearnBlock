from __future__ import print_function, absolute_import
import sys, os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import visual_auxiliary as va

def is_line_crossing(lbot):
	frame = lbot.getImage()
	if frame is not None:
		roisR = va.detect_red_line(frame)
		roisB = va.detect_black_line(frame)
		if roisR[1]>40 and roisB[1]>40:
			return True
	return False
