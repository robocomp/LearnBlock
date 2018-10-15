from __future__ import print_function
import visual_auxiliary as va
import numpy as np

def is_there_red_line(lbot, params=None, verbose=False):
    frame = lbot.getImage()
    rois = va.detect_red_line(frame)
    if verbose:
        print("Red points", rois)
    if rois[np.argmax(rois)]>20:
        return True
    return False