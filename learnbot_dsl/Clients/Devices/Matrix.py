
class Matrix():

    def __init__(self, _setState=None,_setNumber=None,_setText=None, _readState=None):
        self._State = None
        self._setState = _setState
        self._setNumber = _setNumber
        self._setText = _setText
        self._readState = _readState

    def setState(self, _status,_shine):
        if self._setState is not None:
            self._setState(_status,_shine)
            _State = _status
    def setNumber(self, _number,_shine):
        if self.setNumber is not None:
            self._setNumber(_number,_shine)
            _State = _number
    def setText(self, _text,_shine,_column):
        if self._setText is not None:
            self._setText(_text,_shine,_column)
            _State = _text

    def read(self):
        if self._readState is not None:
            self._State = self._readState()

    def getState(self):
        return self._State

