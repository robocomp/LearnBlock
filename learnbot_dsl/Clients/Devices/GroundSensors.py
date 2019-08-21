
class GroundSensors():
    __groundSensor = {"left": None,  
                        "central": None,
                        "right": None}

    def __init__(self, _readFunction):
        self._readDevice = _readFunction

    def set(self, key, value):
        self.__groundSensor[key] = value

    def read(self):
        dictValues = self._readDevice()
        #print(dictValues)
        for key in dictValues:
            self.set(key, dictValues[key])

    def get(self):
        return self.__groundSensor
