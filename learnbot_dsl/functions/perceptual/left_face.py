from __future__ import print_function, absolute_import
import cv2
import numpy as np
import learnbot_dsl.functions.perceptual.visual_auxiliary as va


def left_face(lbot, params=None, verbose=False):
    frame = lbot.getImage()
    mat = va.detect_face(frame)
    if mat[0][0] is not 0 or mat[1][0] is not 0 or mat[2][0] is not 0:
        return True
    return False
