
class LightSensor():
    __lightSensor = 0

    def __init__(self, _readFunction):
        self._readDevice = _readFunction

    def set(self, values):
        self.__lightSensor = values

    def read(self):
        self.set(self._readDevice())

    def get(self):
        return self.__lightSensor
