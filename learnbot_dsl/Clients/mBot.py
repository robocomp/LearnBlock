
from multiprocessing import Value
from signal import ITIMER_REAL

from numpy import append
from learnbot_dsl.Clients.Client import *
from learnbot_dsl.Clients.Devices import *
from learnbot_dsl.functions import getFuntions
import math, traceback, sys, tempfile, os
from threading import Event
import  time

from learnbot_dsl.Clients.Third_Party.MLib.mBot import *

L = 110
MAXSPEED = 1000
CONSVEL = 0.468
CONSGIRO = 0.748


class Robot(Client):
    def __init__(self):
        Client.__init__(self, _miliseconds=10)
        
        self.bot=mBot(self)
        self.groundSensor={}
        self.distanceSensor=0
        self.lightSensor=0
        self.IRSensor=0
        self.callback=False
        self.connectToRobot()

        #Añadiendo dispositivos
        print("Registrando dispositivos")
        #Actuadores
        self.addBase(Base(_callFunction=self.deviceBaseMove))
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedLeft),"Left")
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedRight),"Right")
        self.addSpeaker(Speaker(_sendFrequency=self.devicePlaySound))
        #Sensores
        #self.addIR(Ir(_readFunction=self.deviceReadIRSensor))
        #self.addLight(LightSensor(_readFunction=self.deviceReadLightSensor))
        self.addGroundSensors(GroundSensors(_readFunction=self.deviceReadGroundSensor))
        #self.addDistanceSensors(DistanceSensors(_readFunction=self.deviceReadSonar))
        print("Dispositivos Registrados")
        self.start()

    def connectToRobot(self):
        self.bot.startWithSerial("/dev/ttyUSB1")
        self.bot.doMove(0,0) #parar la base
        time.sleep(0)

    def disconnect(self):
        self.bot.doMove(0,0) #parar la base

    

##############################ACTUADORES###########################
#-------------------------------Base---------------------------
    def deviceBaseMove(self, SAdv, SRot): 
        SRot_rad = math.radians(SRot)
        rot=0
        if SRot != 0.:
            rot = SRot_rad*L/2
        l_wheel_speed = SAdv * CONSVEL+rot*CONSGIRO
        r_wheel_speed = SAdv * CONSVEL-rot*CONSGIRO
        self.bot.doMove(round(l_wheel_speed),round(r_wheel_speed))

#-----------------------------LED---------------------------
    def deviceRGBLedLeft(self, r, g, b):
        self.bot.doRGBLedOnBoard(2,r,g,b)

    def deviceRGBLedRight(self, r, g, b):
        self.bot.doRGBLedOnBoard(1,r,g,b)

#---------------------------Buzzer---------------------------
    def devicePlaySound(self,sound,time):
        self.bot.doBuzzer(sound,time)

#############################SENSORES############################
#-------------------------DistanceSensor---------------------------
    def callbackSonar(self,value):
        print("efectuando callback")
        self.distanceSensor=value
        self.callback=False

    def deviceReadSonar(self):
        self.callback=True  
        self.bot.requestUltrasonicSensor(2,"callbackSonar")
        while self.callback:
            sleep(0.01)
        self.distanceSensor=math.trunc(float(self.distanceSensor)*10.0) 
        print( self.distanceSensor)
        return {"front": [ self.distanceSensor],  # The values must be in mm
                "left": [2000],
                "right": [2000],
                "back": [2000]}   

#---------------------------LineSensor---------------------------
    def callbackGroundSensor(self,value):
        print("efectuando callback")
        self.groundSensor=value
        self.callback=False

    def deviceReadGroundSensor(self):
        IDGround=["left","right"]  
        dicGround={}
        self.callback=True
        self.bot.requestLineFollower(3,"callbackGroundSensor")
        while self.callback:
            sleep(0.01)
        self.groundSensor=floatAbin( self.groundSensor,2)
        print( self.groundSensor)
        for i,k in enumerate(IDGround):
            if self.groundSensor[i]=='1':
                dicGround[k]=100
            else:
                dicGround[k]=0
        print(dicGround) 
        return dicGround 

#--------------------------LightSensor---------------------------
    def callbackLightSensor(self,value):
        print("efectuando callback")
        self.lightSensor=value
        self.callback=False

    def deviceReadLightSensor(self): 
        self.callback=True 
        self.bot.requestLight("callbackLightSensor")
        while self.callback:
            sleep(0.01)
        print( self.lightSensor)
        return self.lightSensor  

#----------------------------IRSensor---------------------------
    def callbackIR(self,value):
        print("efectuando callback")
        self.IRSensor=value
        self.callback=False

    def deviceReadIRSensor(self):  
        self.callback=True 
        self.bot.requestIROnBoard("callbackIR")
        while self.callback:
            sleep(0.01)
        print( self.IRSensor)
        return self.IRSensor 
           

#Funcion de conversión de int a binario
def floatAbin(val,bits):
    groundSensorBin=[]
    valInt=int(val)
    #Convertimos a binario 
    valBin=bin(valInt)
    #eliminamos el caracter 0b
    valBin=valBin.lstrip("0b")
    #Rellenamos de 0 hasta tener todos los bits
    for x in range((bits-1),-1,-1):
        if x>=len(valBin):
            groundSensorBin.append(0)
        else:
            #la lectura de valBin tiene que que ser al reves
            groundSensorBin.append(valBin[len(valBin)-x-1])
    return groundSensorBin

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


