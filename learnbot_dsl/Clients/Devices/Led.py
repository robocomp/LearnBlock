from enum import Enum

class LedStatus(Enum):
    ON = True
    OFF = False

class Led():
    _setState = None
    _readState = None
    _State = None

    def __init__(self, _setState,_readState=None):
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