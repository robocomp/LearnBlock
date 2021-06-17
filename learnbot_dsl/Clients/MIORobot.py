
from learnbot_dsl.Clients.Client import *
from learnbot_dsl.Clients.Devices import *
from learnbot_dsl.functions import getFuntions
import math, traceback, sys, tempfile, os
from threading import Event
import  time

from learnbot_dsl.Clients.Third_Party.MIOLib.MIOBot import *

K = 35
L = 110
MAXSPEED = 1000
CONSVEL = 0.615
CONSGIRO = 0.878


class Robot(Client):
    def __init__(self):
        Client.__init__(self, _miliseconds=100)
        
        self.bot=MIOBot()
        self.groundSensor=0
        self.SonarSensor=0
        self.connectToRobot()

        #Añadiendo dispositivos
        print("Registrando dispositivos")
        self.addBase(Base(_callFunction=self.deviceBaseMove))
       # self.addDistanceSensors(DistanceSensors(_readFunction=self.deviceReadSonar))
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedDown),"Down")
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedLeft),"Left")
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedCentre),"Centre")
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedRight),"Right")
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedUp),"Up")
        
        #self.addGroundSensors(GroundSensors(_readFunction=deviceReadGroundSensors))
        print("Dispositivos Registrados")
        self.start()

    def connectToRobot(self):
        self.bot.startWithSerial("/dev/ttyUSB2")
        time.sleep(4)
    def disconnect(self):
        self.bot.doMove(0,0) #parar la base
        
        

    def deviceBaseMove(self, SAdv, SRot):
    
        SRot_rad = math.radians(SRot)
        rot=0
        if SRot != 0.:
                        
            rot = SRot_rad*L/2

        
        l_wheel_speed = SAdv * CONSVEL+rot*CONSGIRO
        r_wheel_speed = SAdv * CONSVEL-rot*CONSGIRO
        self.bot.doMove(round(l_wheel_speed),round(r_wheel_speed))
    

    #############Funciones Led#################
    def deviceRGBLedDown(self, r, g, b):
        self.bot.doRGBLedOnBoard(1,r,g,b)

    def deviceRGBLedLeft(self, r, g, b):
        self.bot.doRGBLedOnBoard(2,r,g,b)

    def deviceRGBLedCentre(self, r, g, b):
        self.bot.doRGBLedOnBoard(3,r,g,b)

    def deviceRGBLedRight(self, r, g, b):
        self.bot.doRGBLedOnBoard(4,r,g,b)

    def deviceRGBLedUp(self, r, g, b):
        self.bot.doRGBLedOnBoard(5,r,g,b)

    def deviceReadGroundSensors(self):
        self.bot.requestLineFollower(self.bot,3,callbackGroundSensor)
        return{"left": 100 if bin(ground)[0]==1 else 0,  
                 "central": 100 if bin(ground)[1]==1 else 0,
                 "right":100 if bin(ground)[2]==1 else 0}

    def deviceReadSonar(self):  
        self.bot.requestUltrasonicSensor(2,callbackSonar)
        time.sleep(0.1)
        print( distance)
        return {"front": [ distance],  # The values must be in mm
                "left": [2000],
                "right": [2000],
                "back": [2000]}
    '''
    def callbackSonar(self,value):
        print (value)
        self.distanceSensor=math.trunc(float(value)*10.0) 

    def deviceReadSonar(self):  
        self.bot.requestUltrasonicSensor(2,"callbackSonar",self)
        time.sleep(0.1)
        print( self.distanceSensor)
        return {"front": [ self.distanceSensor],  # The values must be in mm
                "left": [2000],
                "right": [2000],
                "back": [2000]}
     '''
'''
def callBack(method):
    return method()   

def callBack3(value):
    return value

def callBack2(o,method):
    m=getattr(o,method)
    return m             
'''
def callbackSonar(value):
    global distance
    print (value)
    distance=math.trunc(float(value)*10.0)
        

def callbackGroundSensor(value):
    global ground
    ground=value

if __name__ == '__main__':
    try:
        robot = Robot()
    except Exception as e:
        print("hay un Error")
        traceback.print_exc()
        raise (e)
    print(dir(robot))
    time_global_start = time.time()

    robot.stop_bot()


    def elapsedTime(umbral):
        global time_global_start
        time_global = time.time() - time_global_start
        return time_global > umbral


