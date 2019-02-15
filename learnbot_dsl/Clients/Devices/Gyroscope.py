
class Gyroscope():
    '''
    Gyroscope is a class that contain the values rx, ry, rz of a Gyroscope in rad.
    '''
    rx = None
    ry = None
    rz = None

    def __init__(self, _readFunction):
        self.__readDevice = _readFunction

    def set(self, _rx, _ry, _rz):
        self.rx, self.ry, self.rz = _rx, _ry, _rz

    def get(self):
        return self.rx, self.ry, self.rz

    def read(self):
        _rx, _ry, _rz = self.__readDevice()
        self.set(_rx, _ry, _rz)