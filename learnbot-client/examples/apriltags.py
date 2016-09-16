#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import urllib
import numpy as np

encontrado=False
cmd = './apriltags_ImagePython 320 240 tempImage.jpg && rm tempImage.jpg'
while encontrado is False:
  stream = urllib.urlopen('http://odroid.local:8080/?action=stream')
  bytes=''
  Frame = False
  while Frame is False:
    bytes += stream.read(1024)	    
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
      jpg = bytes[a:b+2]
      bytes = bytes[b+2:]
      image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
      Frame = True
      cv2.imwrite("tempImage.jpg", image);
      os.system(cmd)
      img = cv2.imread('result.jpg');
      cv2.imshow('result.jpg',img)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

