import sys, time
import LearnBotClient

# Ctrl+c handling
import signal
#import cv2
signal.signal(signal.SIGINT, signal.SIG_DFL)


class MiClase(LearnBotClient.Client):
  def __init__(self):
    pass

  def code(self):
    while True:
      image = self.getImage()
#      cv2.imshow('Frame capture',image)
      time.sleep(5)

miclase = MiClase()
miclase.main(sys.argv)