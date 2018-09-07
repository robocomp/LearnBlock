import numpy as np
import imutils
import cv2

net = cv2.dnn.readNetFromCaffe('/home/robocomp/robocomp/components/learnbot/components/emotionrecognition2/assets/deploy.prototxt.txt', '/home/robocomp/robocomp/components/learnbot/components/emotionrecognition2/assets/res10_300x300_ssd_iter_140000.caffemodel')

def detect(image):
	faces = []
	(h, w) = image.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

	net.setInput(blob)
	detections = net.forward()

	for i in range(0, detections.shape[2]):

		confidence = detections[0, 0, i, 2]

		if confidence > 0.8:
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			faces.append(box.astype("int"))

	return faces