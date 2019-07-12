from __future__ import print_function, absolute_import
import cv2, os
import numpy as np

LL_red = (0, 50, 100)
LU_red = (10, 255, 255)

LL_red2 = (170, 50, 100)
LU_red2 = (180, 255, 255)

LL_blue = (100, 50, 50)
LU_blue = (130, 255, 255)

def countRois(binary):
    rois = [0, 0, 0]
    rois[0] = cv2.countNonZero(binary[15:225, 0:120])
    rois[1] = cv2.countNonZero(binary[15:225, 120:200])
    rois[2] = cv2.countNonZero(binary[15:225, 200:320])
    return rois

def detect_black_line(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    err, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    return countRois(binary)

def detect_red_line(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    binary = cv2.inRange(hsv, LL_red, LU_red)
    binary2 = cv2.inRange(hsv, LL_red2, LU_red2)
    binary = binary + binary2
    err, binary = cv2.threshold(binary, 100, 255, cv2.THRESH_BINARY)
    binary = cv2.dilate(binary, None, iterations=3)
    return countRois(binary)

def detect_blue_line(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    binary = cv2.inRange(hsv, LL_blue, LU_blue)
    err, binary = cv2.threshold(binary, 100, 255, cv2.THRESH_BINARY)
    binary = cv2.dilate(binary, None, iterations=3)
    return countRois(binary)

path = os.path.dirname(os.path.realpath(__file__))

face_cascade = cv2.CascadeClassifier(os.path.join(path, "haarcascade_frontalface_alt.xml"))
face_cascade2 = cv2.CascadeClassifier(os.path.join(path, "haarcascade_profileface.xml"))

def detect_face(frame):
    height, width, channels = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces2 = face_cascade2.detectMultiScale(gray, 1.3, 5)
    # Dibujamos un rectangulo en las coordenadas de cada rostro
    mat = [[0, 0, 0] for x in range(3)]
    for (x, y, w, h) in faces:
        mat[(y + h // 2) // (height // 3)][(x + w // 2) // (width // 3)] += 1
    for (x, y, w, h) in faces2:
        mat[(y + h // 2) // (height // 3)][(x + w // 2) // (width // 3)] += 1
    return mat
