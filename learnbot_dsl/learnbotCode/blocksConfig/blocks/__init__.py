import inspect
import os
# import cv2, time
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

__all__ = ["pathBlocks", "HUE_CONTROL", "HUE_MOTOR", "HUE_PERCEPTUAL", "HUE_PROPIOPERCEPTIVE", "HUE_OPERATOR", "HUE_EXPRESS", "HUE_OTHERS", "HUE_USERFUNCTION", "HUE_VARIABLE", "HUE_STRING", "HUE_NUMBER", "HUE_WHEN"]

pathBlocks = path





# HUE values
HUE_CONTROL = 0
HUE_MOTOR = 0
HUE_PERCEPTUAL = 40
HUE_PROPIOPERCEPTIVE = 80
HUE_OPERATOR = 120
HUE_EXPRESS = 160
HUE_OTHERS = 200
HUE_USERFUNCTION = 240
HUE_VARIABLE = 10
HUE_STRING = 20
HUE_NUMBER = 30
HUE_WHEN = 50

# for x in range(256):
#     print x
#     im = cv2.imread("block1azul.png", cv2.IMREAD_UNCHANGED)
#     r,g,b,a = cv2.split(im)
#     rgb = cv2.merge((r,g,b))
#     hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
#     h,s,v = cv2.split(hsv)
#     h=h+x
#     s=s+130
#     hsv = cv2.merge((h,s,v))
#     im = cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)
#     r, g, b = cv2.split(im)
#     im = cv2.merge((r, g, b, a))
#     cv2.imshow("a", im)
#     while True:
#         if cv2.waitKey(33) == ord('a'):
#             break