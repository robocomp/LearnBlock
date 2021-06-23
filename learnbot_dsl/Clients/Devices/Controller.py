
class Controller():
    __button = {"lUp": False, 
                "lLeft": False,
                "lRight": False,
                "lDown": False,
                "rUp": False, 
                "rLeft": False,
                "rRight": False,
                "rDown": False }

    def __init__(self, _readFunction):
        self._readDevice = _readFunction

    def set(self, key, values):
        self.__button[key] = values

    def read(self):
        buttonValues = self._readDevice()
        for key in buttonValues:
            self.set(key, buttonValues[key])

    def get(self):
        return self.__button
