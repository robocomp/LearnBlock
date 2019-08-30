
class Acelerometer():
    '''
    Acelerometer is a class that contain the values rx, ry, rz of a Acelerometer in degrees.
    '''
    _x = None
    _y = None
    _z = None

    def __init__(self, _readFunction):
        self._readDevice = _readFunction

    def set(self, _x, _y, _z):
        self._x, self._y, self._z = _x, _y, _z

    def get(self):
        return self._x, self._y, self._z

    def read(self):
        _x, _y, _z = self._readDevice()
        self.set(_x, _y, _z)
