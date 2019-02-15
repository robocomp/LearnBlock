import copy, numpy as np
from threading import Lock

class Camera():
    '''
    Camera devices.
    '''
    __image = np.zeros((240, 320, 3), np.uint8)     # RGB image 240x320
    __newImageAvailable = False
    __mutexRead = Lock()
    def __init__(self, _readFunction):
        self._readDevice = _readFunction

    def read(self):
        self.__mutexRead.acquire()
        img, new = self._readDevice()
        if new is True:
            self.__image = img
            self.__newImageAvailable = True
        self.__mutexRead.release()

    def getImage(self):
        self.__mutexRead.acquire()
        simage = copy.copy(self.__image)
        self.__mutexRead.release()
        return simage

    def disableNewImageAvailable(self):
        self.__newImageAvailable = False