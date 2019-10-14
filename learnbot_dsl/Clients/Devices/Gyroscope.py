
class Gyroscope():
    '''
    Gyroscope interface class.
    This class reads, updates and returns the rotation (degrees) of the robotic platform on a given axis.
    The key of the device used in the addGyroscope method should be related to the rotation axis: "X-AXIS", "Y-AXIS", "Z-AXIS"
    '''
    rot = None

    def __init__(self, _readFunction, _resetFunction):
        self.__readDevice = _readFunction
        self.__resetDevice = _resetFunction

    def set(self, _rot):
        self.rot = _rot

    def get(self):
        if self.rot is None:
            self.read()
        return self.rot

    def read(self):
        _rot = self.__readDevice()
        if _rot is not None:
            self.set(_rot)

    def reset(self):
        self.__resetDevice()
