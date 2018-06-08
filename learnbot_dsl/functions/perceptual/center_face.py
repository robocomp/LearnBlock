from __future__ import print_function
import cv2
import numpy as np
import visual_auxiliary as va


def right_face(lbot, params=None, verbose=False):
    frame = lbot.getImage()
    mat = va.detect_face(frame)
    if mat[1][1] is not 0:
        return True
    return False
