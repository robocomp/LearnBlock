from enum import Enum

class LedStatus(Enum):
    ON = True
    OFF = False


class Led():

    def __init__(self, _setState=None, _readState=None):
        self._State = None
        self._setState = _setState
        self._readState = _readState

    def setState(self, _status):
        self._setState(_status)
        _State = _status

    def read(self):
        if self._readState is not None:
            self._State = self._readState()

    def getState(self):
        return self._State


class RGBLed():

    def __init__(self, _setColorState=None, _readState=None):
        self._State = None
        self._readState = _readState
        self._setColorState = _setColorState

    def setColorState(self, _r, _g, _b):
        if self._setColorState is not None:
            self._setColorState(_r, _g, _b)
            self._State = (_r, _g, _b)

    def read(self):
        if self._readState is not None:
            self._State = self._readState()

    def getState(self):
        return self._State