from learnbot_dsl.Clients.Devices.Base import Base
from learnbot_dsl.Clients.Devices.DistanceSensors import DistanceSensors
from learnbot_dsl.Clients.Devices.Gyroscope import Gyroscope
from learnbot_dsl.Clients.Devices.Acelerometer import Acelerometer
from learnbot_dsl.Clients.Devices.Camera import Camera
from learnbot_dsl.Clients.Devices.JointMotor import JointMotor
from learnbot_dsl.Clients.Devices.Display import Display
from learnbot_dsl.Clients.Devices.Led import Led, LedStatus
from learnbot_dsl.Clients.Devices.Speaker import Speaker

from enum import Enum


__all__ = ['Display', 'Base', 'DistanceSensors', 'Gyroscope', 'Acelerometer', 'Camera', 'Emotions', 'JointMotor', 'Speaker', 'Led', 'LedStatus']

class Emotions(Enum):
    NoneEmotion = -1
    Fear = 0
    Surprise = 1
    Anger = 2
    Sadness = 3
    Disgust = 4
    Joy = 5
    Neutral = 6