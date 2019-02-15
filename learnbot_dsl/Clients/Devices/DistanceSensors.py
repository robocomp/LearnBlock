
class DistanceSensors():
    __distanceSensor = {"front": None,  # The values must be in mm
                        "left": None,
                        "right": None,
                        "back": None,
                        "bottom": None}

    def __init__(self, _readFunction):
        self._readDevice = _readFunction

    def set(self, key, values):
        self.__distanceSensor[key] = values

    def read(self):
        dictValues = self._readDevice()
        for key in dictValues:
            self.set(key, dictValues[key])

    def get(self):
        return self.__distanceSensor
