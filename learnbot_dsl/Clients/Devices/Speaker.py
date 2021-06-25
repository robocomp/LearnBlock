
class Speaker():
    _sendAudio = None
    _sendText = None
    _sendFrequency = None

    def __init__(self, _sendAudio = None, _sendText = None,_sendFrequency = None):
        self._sendAudio = _sendAudio
        self._sendText = _sendText
        self._sendFrequency = _sendFrequency

    def sendAudio(self, _audiodata):
        if self._sendAudio is not None:
            self._sendAudio(_audiodata)

    def sendText(self, _text):
        if self._sendText is not None:
            self._sendText(_text)

    def sendFrequency(self, _frequency,_time):
        if self._sendFrequency is not None:
            self._sendFrequency(_frequency,_time)
