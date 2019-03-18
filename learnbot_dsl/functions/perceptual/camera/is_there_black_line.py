from __future__ import print_function, absolute_import
import sys, os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import visual_auxiliary as va
import numpy as np

def is_there_black_line(lbot, params=None, verbose=False):
    frame = lbot.getImage()
    rois = va.detect_black_line(frame)
    if verbose:
        print("Black points", rois)
    if rois[np.argmax(rois)]>20:
        return True
    return False