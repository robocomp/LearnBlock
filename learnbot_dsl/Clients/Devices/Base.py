
class Base():

    """
    Base is the differential base of the robot.
    """
    __Sadv = 0  # in mm/s
    __Srot = 0  # in degrees/s

    def __init__(self, _callFunction):
        self.__callDevice = _callFunction

    def move(self, _Sadv, _Srot):
        self.__Sadv, self.__Srot = _Sadv, _Srot
        self.__callDevice(_Sadv, _Srot)

    def adv(self):
        return self.__Sadv

    def rot(self):
        return self.__Srot
