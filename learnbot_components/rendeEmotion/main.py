import cv2, numpy as np
from copy import copy,deepcopy
from random import randint
from PIL import Image, ImageDraw
#
# img=np.zeros((100,100))
#
# radius=5
# axes = (radius,radius)
# angle=90;
# startAngle=0;
# endAngle=180;
# center=(50,50)
# color=255
#
# cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color,-1)
#
#
#
# cv2.imshow("emotion", img)
# cv2.waitKey(0)

Alegria = {"ojoI"   : [(121,142),(45,45),180,30,330],
           "ojoD"   : [(357,142),(45,45),0,0,360],
           "cejaIs" : [[64,75], [114,5], [179,57]],
           "cejaIi" : [[179, 57], [114, 25], [64, 75]],
           "cejaDs" : [[302, 57], [362, 5], [417, 75]],
           "cejaDi" : [[417, 75], [362, 25], [302, 57]],
           "labioS" : [[176,241],[220,310],[260,310],[301,241]],
           "labioI" : [[301,241],[260,330],[220,330],[176,241]]
           }

OJOI = [(121,142),(45,45),90,30,330]
OJOD = [(357,142),(45,45),90,30,330]

CEJAI1=[[64,75], [114,5], [179,57]]
CEJAI2=[[179,57], [114,25], [64,75]]

CEJAD1=[[302,57], [362,5], [417,75]]
CEJAD2=[[417,75], [362,25], [302,57]]

BOCA1 =[[176,241],[220,310],[260,310],[301,241]]
BOCA2=[[301,241],[260,330],[220,330],[176,241]]
def bezier(p1, p2, t):
    t = t / 10.
    diff = (p2[0] - p1[0], p2[1] - p1[1])
    return [p1[0] + diff[0] * t, p1[1] + diff[1] * t]


def getPointsBezier(points):
    bezierPoints = list()
    pointsCopy = copy(points)
    for t in range(11):
        while len(points)!=1:
            newPoints = list()
            p1=points[0]
            for p2 in points[1:]:
                newPoints.append(bezier(p1,p2,t))
                p1=p2
            points=newPoints
        bezierPoints.append(tuple(points[0]))
        points=pointsCopy
    return bezierPoints

class emotion:
    def __init__(self, cejaI1,cejaI2, cejaD1, cejaD2, ojoI, ojoD, irisI, irisD, boca1,boca2):
        self.cejaI1 = cejaI1
        self.cejaI2 = cejaI2
        self.cejaD1 = cejaD1
        self.cejaD2 = cejaD2
        self.ojoI = ojoI
        self.ojoD = ojoD
        self.irisI = irisI
        self.irisD = irisD
        self.boca1 = boca1
        self.boca2 = boca2

    def render2(self):
        boca1 = randint(-5, 5)
        boca2 = randint(-5, 5)
        img= Image.new('RGB', (480,320), 'white')
        draw = ImageDraw.Draw(img)
        draw.polygon(getPointsBezier(self.cejaI1) + getPointsBezier(self.cejaI2),fill=1)
        draw.polygon(getPointsBezier(self.cejaD1) + getPointsBezier(self.cejaD2),fill=1)

        draw.ellipse([((91,92)),((171,184))],fill=1)


        copyboca1 = deepcopy(self.boca1)
        copyboca2 = deepcopy(self.boca2)
        for p in copyboca1[1:-1]:
            p[1] += boca1
        for p in copyboca2[1:-1]:
            p[1] += boca2
        draw.polygon(getPointsBezier(copyboca1) + getPointsBezier(copyboca2), fill=1)
        img.show()

    def render(self):
        boca1=randint(-5, 5)
        boca2 = randint(-5, 5)
        img = np.zeros((320, 480, 3), np.uint8)
        img[:] = (255,255,255)

        cv2.fillPoly(img, np.int32([np.array(getPointsBezier(self.cejaI1)+getPointsBezier(self.cejaI2))]), (0, 0, 0))
        cv2.fillPoly(img, np.int32([np.array(getPointsBezier(self.cejaD1)+getPointsBezier(self.cejaD2))]), (0, 0, 0))

        # cv2.polylines(img, self.ojoI, 1, (0, 0, 0))
        # cv2.polylines(img, self.ojoD, 1, (0, 0, 0))
        #
        # cv2.circle(img,(357,142),45,(0,0,0),-1)
        # cv2.circle(img,(121,142),45,(0,0,0),-1)
        cv2.ellipse(img, self.ojoD[0], self.ojoD[1], self.ojoD[2], self.ojoD[3], self.ojoD[4], (0,0,0),-1)
        cv2.ellipse(img, self.ojoI[0], self.ojoI[1], self.ojoI[2], self.ojoI[3], self.ojoI[4], (0,0,0),-1)

        # cv2.circle(img,self.irisI[0],self.irisI[1],(255,255,255))
        # cv2.circle(img,self.irisD[0],self.irisD[1],(255,255,255))
        #
        copyboca1 = deepcopy(self.boca1)
        copyboca2 = deepcopy(self.boca2)
        for p in copyboca1[1:-1]:
            p[1]+=boca1
        for p in copyboca2[1:-1]:
            p[1]+=boca2
        # cv2.polylines(img, np.int32([np.array(getPointsBezier(copyboca1)+getPointsBezier(copyboca2))]), 1, (255, 255, 255),5)
        cv2.fillPoly(img, np.int32([np.array(getPointsBezier(copyboca1)+getPointsBezier(copyboca2))]), (0, 0, 0))
        # cv2.polylines(img, np.int32([np.array(getPointsBezier(copyboca2))]), 0, (255, 255, 255))
        im= Image.fromarray(img)
        im.show("prueba")
        pass




import time
e = emotion(CEJAI1,CEJAI2,CEJAD1,CEJAD2, OJOD,OJOI,None,None,BOCA1,BOCA2 )
e.render2()
exit(0)
while True:
    e.render()
    time.sleep(0.05)