import inspect
import os
# import cv2, time
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

__all__ = ["pathBlocks", "HUE_CONTROL", "HUE_MOTOR", "HUE_PERCEPTUAL", "HUE_PROPIOPERCEPTIVE", "HUE_OPERATOR", "HUE_EXPRESS", "HUE_OTHERS", "HUE_USERFUNCTION", "HUE_VARIABLE", "HUE_STRING", "HUE_NUMBER", "HUE_WHEN"]

pathBlocks = path


# HUE values
HUE_CONTROL = 0

HUE_MOTOR = 0
HUE_PERCEPTUAL = 60
HUE_PROPIOPERCEPTIVE = 80
HUE_OPERATOR = 120
HUE_EXPRESS = 160
HUE_OTHERS = 200
HUE_USERFUNCTION = 240
HUE_VARIABLE = 20
HUE_STRING = 75
HUE_NUMBER = 40
HUE_WHEN = 50
