from __future__ import print_function, absolute_import
import sys, os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import visual_auxiliary as va


def is_center_face(lbot):
    frame = lbot.getImage()
    if frame is not None:
        mat = va.detect_face(frame)
        if mat[1][1] is not 0:
            return True
    return False
