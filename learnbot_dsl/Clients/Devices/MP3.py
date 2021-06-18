
class MP3():

    def __init__(self, _sendAudio = None,_sendAction = None,_modifyVolume = None, _modifyEQ = None,_modifyLoop = None):
        self._sendAudio = _sendAudio
        self._sendAction = _sendAction
        self._modifyVolume = _modifyVolume
        self._modifyEQ = _modifyEQ
        self._modifyLoop = _modifyLoop

    def sendAudio(self, _folder, _audiodata):
        if self._sendAudio is not None:
            self._sendAudio(_folder,_audiodata)

    def sendAction(self, _action):
        if self._sendAction is not None:
            self._sendAction(_action)
    
    def modifyVolume(self, _volume):
        if self._modifyVolume is not None:
            self._modifyVolume(_volume)

    def modifyEQ(self, _EQ):
        if self._modifyEQ is not None:
            self._modifyEQ(_EQ)

    def modifyLoop(self, _loop):
        if self._modifyLoop is not None:
            self._modifyLoop(_loop)

