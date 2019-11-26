from __future__ import print_function, absolute_import
import sys, os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import visual_auxiliary as va
import numpy as np

def is_there_blue_line(lbot):
    frame = lbot.getImage()
    if frame is not None:
        rois = va.detect_blue_line(frame)
        if rois[np.argmax(rois)]>20:
            return True
    return False
