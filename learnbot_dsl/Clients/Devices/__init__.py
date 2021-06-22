from learnbot_dsl.Clients.Devices.Base import Base
from learnbot_dsl.Clients.Devices.DistanceSensors import DistanceSensors
from learnbot_dsl.Clients.Devices.GroundSensors import GroundSensors
from learnbot_dsl.Clients.Devices.Gyroscope import Gyroscope
from learnbot_dsl.Clients.Devices.Acelerometer import Acelerometer
from learnbot_dsl.Clients.Devices.Camera import Camera
from learnbot_dsl.Clients.Devices.JointMotor import JointMotor
from learnbot_dsl.Clients.Devices.Display import Display
from learnbot_dsl.Clients.Devices.Led import Led, LedStatus, RGBLed
from learnbot_dsl.Clients.Devices.Speaker import Speaker
from learnbot_dsl.Clients.Devices.Matrix import Matrix
from learnbot_dsl.Clients.Devices.MP3 import MP3
from learnbot_dsl.Clients.Devices.Ir import Ir
from learnbot_dsl.Clients.Devices.LightSensor import LightSensor
from learnbot_dsl.Clients.Devices.Controller import Controller
from enum import Enum


__all__ = ['Display', 'Base', 'DistanceSensors', 'GroundSensors', 'Gyroscope', 'Acelerometer', 'Camera', 'Emotions', 'JointMotor', 'Speaker', 'Led', 'RGBLed', 'LedStatus','Matrix','MP3','Ir','LightSensor','Controller']

class Emotions(Enum):
    NoneEmotion = -1
    Fear = 0
    Surprise = 1
    Anger = 2
    Sadness = 3
    Disgust = 4
    Joy = 5
    Neutral = 6
