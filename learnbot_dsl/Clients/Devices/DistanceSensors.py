
class DistanceSensors():
    __distanceSensor = {"front": [0],  # The values must be in mm
                        "left": [0],
                        "right": [0],
                        "back": [0]
                       }

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
