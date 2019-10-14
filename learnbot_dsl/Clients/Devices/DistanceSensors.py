
class DistanceSensors():
    __distanceSensor = {"front": [2000],  # The values must be in mm
                        "left": [2000],
                        "right": [2000],
                        "back": [2000]
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
