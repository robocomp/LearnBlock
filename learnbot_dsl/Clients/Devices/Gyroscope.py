
class Gyroscope():
    '''
    Gyroscope is a class that contain the values rx, ry, rz of a Gyroscope in degrees.
    '''
    rx = None
    ry = None
    rz = None

    def __init__(self, _readFunction, _resetFunction):
        self.__readDevice = _readFunction
        self.__resetDevice = _resetFunction

    def set(self, _rx, _ry, _rz):
        self.rx, self.ry, self.rz = _rx, _ry, _rz

    def get(self):
        return self.rx, self.ry, self.rz

    def read(self):
        _rx, _ry, _rz = self.__readDevice()
        self.set(_rx, _ry, _rz)

    def reset(self):
        self.__resetDevice()
