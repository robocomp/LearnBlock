
class Speaker():
    _sendAudio = None
    _sendText = None

    def __init__(self, _sendAudio = None, _sendText = None):
        self._sendAudio = _sendAudio
        self._sendText = _sendText

    def sendAudio(self, _audiodata):
        if self._sendAudio is not None:
            self._sendAudio(_audiodata)

    def sendText(self, _text):
        if self._sendText is not None:
            self._sendText(_text)
