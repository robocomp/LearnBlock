

class Display():

    def __init__(self, _setEmotion, _setImage):
        self._setEmotion = _setEmotion
        self._setImage = _setImage

    def setEmotion(self, _emotion):
        self._setEmotion(_emotion)

    def setImage(self, _img):
        self._setImage(_img)