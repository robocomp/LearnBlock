
class JointMotor():

    _angle = 0

    def __init__(self, _callDevice, _readDevice):
        self._callDevice = _callDevice
        self._readDevice = _readDevice

    def sendAngle(self, _angle):
        self._callDevice(_angle)
        self._angle = _angle

    def getAngle(self):
        return self._angle

    def read(self):
        _angle = self._readDevice()
