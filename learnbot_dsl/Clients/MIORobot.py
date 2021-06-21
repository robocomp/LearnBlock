
from multiprocessing import Value
from signal import ITIMER_REAL

from numpy import append
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
        
        self.bot=MIOBot(self)
        self.groundSensor={}
        self.distanceSensor=0
        self.lightSensor=0
        self.IRSensor=0
        self.controllerSensor={}
        self.connectToRobot()

        #Añadiendo dispositivos
        print("Registrando dispositivos")
        #Actuadores
        self.addBase(Base(_callFunction=self.deviceBaseMove))
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedDown),"Down")
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedLeft),"Left")
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedCentre),"Centre")
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedRight),"Right")
        self.addRGBLed(RGBLed(_setColorState=self.deviceRGBLedUp),"Up")
        self.addSpeaker(Speaker(_sendAudio=self.devicePlaySound))
        self.addMatrix(Matrix(_setState=self.deviceMatrixIcon,_setNumber=self.deviceMatrixNum,_setText=self.deviceMatrixText))
        self.addMP3(MP3(_sendAudio = self.deviceMP3Audio,_sendAction = self.deviceMP3Action,_modifyVolume = self.deviceMP3Volume, _modifyEQ = self.deviceMP3EQ,_modifyLoop = self.deviceMP3Loop))
        #Sensores
        self.addIR(IR(_readFunction=self.deviceReadIRSensor))
        self.addLight(LightSensor(_readFunction=self.deviceReadLightSensor))
       # self.addController(Controller(_readFunction=self.deviceReadControllerSensor))
        self.addGroundSensors(GroundSensors(_readFunction=self.deviceReadGroundSensor))
        self.addDistanceSensors(DistanceSensors(_readFunction=self.deviceReadSonar))
        print("Dispositivos Registrados")
        self.start()

    def connectToRobot(self):
        self.bot.startWithSerial("/dev/ttyUSB0")
        time.sleep(4)
    def disconnect(self):
        self.bot.doMove(0,0) #parar la base
        self.bot.doMusicAction(4,"Stop")
        
        
    ###############################ACTUADORES###########################3
    def deviceBaseMove(self, SAdv, SRot): 
        SRot_rad = math.radians(SRot)
        rot=0
        if SRot != 0.:
            rot = SRot_rad*L/2
        l_wheel_speed = SAdv * CONSVEL+rot*CONSGIRO
        r_wheel_speed = SAdv * CONSVEL-rot*CONSGIRO
        self.bot.doMove(round(l_wheel_speed),round(r_wheel_speed))

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

    def devicePlaySound(self,sound):
        self.bot.doBuzzer(sound)

    def deviceMatrixNum(self,number,shine):
        print(number, " on matrix")
        self.bot.doMatrixNumber(1,number,shine)

    def deviceMatrixText(self,text,shine,column):
        print(text, " on matrix")
        self.bot.doMatrixWord(1,text,column,shine)

    def deviceMatrixIcon(self,routeIcon,shine):
        matriz=[]
        fichero = open("/home/alfith/Documentos/Robolab/LearnBlock/learnbot_dsl/Clients/Third_Party/MIOLib/icon/"+routeIcon+".txt", 'r')
        i = 0
        #Lectura de fichero y traspase a la matriz
        for lineas in fichero:
            if i < 8:
                matriz.append([])
            #Remplazamos los retornos de carro por ","
            lineas = lineas.replace('\n', ',')
            #Remplazamos las comillas por separadores
            lineas_separadas = lineas.split(',')
            #Cargamos en la matriz
            for elemento in lineas_separadas:
                if(elemento.isdigit()):
                    elemento_entero = int(elemento)
                    matriz[i].append(elemento_entero)
            i += 1
        #print (matriz)
        self.bot.doMatrixIcon(1,matriz,shine)


    def deviceMP3Audio(self,folder,audio):
        self.bot.doMusicSelect(4,folder,audio)
    
    def deviceMP3Volume(self,volume):
        self.bot.doMusicVol(4,volume)

    def deviceMP3Action(self,action):
        self.bot.doMusicAction(4,action)

    def deviceMP3EQ(self,EQ):
        self.bot.doMusicEQ(4,EQ)

    def deviceMP3Loop(self,loop):
        self.bot.doMusicLoop(4,loop)

    ##################SENSORES############################
    def callbackSonar(self,value):
        self.distanceSensor=math.trunc(float(value)*10.0) 

    def deviceReadSonar(self):  
        self.bot.requestUltrasonicSensor(2,"callbackSonar")
        time.sleep(0.1)
        print( self.distanceSensor)
        return {"front": [ self.distanceSensor],  # The values must be in mm
                "left": [2000],
                "right": [2000],
                "back": [2000]}   

    def callbackGroundSensor(self,value):
        print(value)
        groundSensorBin={}
        valBin=bin(value)
        valBin=valBin.reverse()
        #bin() devuelve 0b... hay que rellenar los ceros que no haya
        for x in range(3):
            if x>=valBin-2:
               groundSensorBin.append(0)
            else:
                groundSensorBin.append(valBin[x+2])
        self.groundSensor=groundSensorBin    

    def deviceReadGroundSensor(self):  
        self.bot.requestLineFollower(3,"callbackGroundSensor")
        time.sleep(0.1)
        print( self.groundSensor)
        #cuidado porque utilizamos la funcion bin() y esta tiene en sus 
        # dos primeras posiciones "0b"
        return {"left": [ self.groundSensor[2]],  
                "central": [self.groundSensor[3]],
                "right": [self.groundSensor[4]]}  

    def callbackLightSensor(self,value):
        self.lightSensor=value

    def deviceReadLightSensor(self):  
        self.bot.requestLight("callbackLightSensor")
        time.sleep(0.1)
        print( self.lightSensor)
        return self.lightSensor  

    def callbackIR(self,value):
        self.IRSensor=value

    def deviceReadIRSensor(self):  
        self.bot.requestIROnBoard("callbackIR")
        time.sleep(0.1)
        print( self.IRSensor)
        return self.IRSensor 

    def callbackController(self,value):
        print(value)
        self.controllerSensor=bin(value)
        

    def deviceReadControllerSensor(self):  
        self.bot.requestButton(4,"callbackController")
        time.sleep(0.1)
        print( self.controllerSensor)
        return {"lUp": self.controllerSensor[0], 
                "lLeft": self.controllerSensor[1],
                "lRight": self.controllerSensor[2],
                "lback": self.controllerSensor[3],
                "rUp": self.controllerSensor[4], 
                "rLeft": self.controllerSensor[5],
                "rRight": self.controllerSensor[6],
                "rback": self.controllerSensor[7]}              

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


