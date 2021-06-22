
class Ir():

    __codeIR = 0

    def __init__(self, _readFunction=None,_sendFunction=None):
        self._readDevice = _readFunction
        self._sendDevice = _sendFunction

    def send(self, values):
        if self._setDevice is not None:
            self._sendDevice(value)

    def set (self, value):
        self.__codeIR = value

    def read(self):
        if self._readDevice is not None:
            self.set(self._readDevice())

    def get(self):
        return self.__codeIR


