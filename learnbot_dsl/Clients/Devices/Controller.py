
class Controller():
    __button = {"lUp": False, 
                "lLeft": False,
                "lRight": False,
                "lback": False,
                "rUp": False, 
                "rLeft": False,
                "rRight": False,
                "rback": False }

    def __init__(self, _readFunction):
        self._readDevice = _readFunction

    def set(self, key, values):
        self.__button[key] = values

    def read(self):
        buttonValues = self._readDevice()
        for key in dictValues:
            self.set(key, buttonValues[key])

    def get(self):
        return self.__button
