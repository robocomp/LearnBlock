
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

L = 110
MAXSPEED = 1000
CONSVEL = 0.505
CONSGIRO = 0.74


class Robot(Client):
    def __init__(self):
        Client.__init__(self, _miliseconds=10)
        
        self.bot=MIOBot(self)
        self.groundSensor={}
        self.distanceSensor=0
        self.lightSensor=0
        self.IRSensor=0
        self.controllerSensor={}
        self.callback=False
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
        #self.addIR(Ir(_readFunction=self.deviceReadIRSensor))
        #self.addLight(LightSensor(_readFunction=self.deviceReadLightSensor))
        #self.addController(Controller(_readFunction=self.deviceReadControllerSensor))
        self.addGroundSensors(GroundSensors(_readFunction=self.deviceReadGroundSensor))
        #self.addDistanceSensors(DistanceSensors(_readFunction=self.deviceReadSonar))
        print("Dispositivos Registrados")
        self.start()

    def connectToRobot(self):
        self.bot.startWithSerial("/dev/ttyUSB0")
        self.bot.doMove(0,0) #parar la base
        self.bot.doMusicAction(4,"Stop")
        self.bot.doBuzzer("Stop")
        time.sleep(0)

    def disconnect(self):
        self.bot.doMove(0,0) #parar la base
        self.bot.doMusicAction(4,"Stop")
        self.bot.doBuzzer("Stop")
        
    

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

#---------------------------Buzzer---------------------------
    def devicePlaySound(self,sound):
        self.bot.doBuzzer(sound)

#--------------------------Matrix---------------------------
    def deviceMatrixNum(self,number,shine):
        print(number, " on matrix")
        self.bot.doMatrixNumber(1,number,shine)

    def deviceMatrixText(self,text,shine,column):
        print(text, " on matrix")
        self.bot.doMatrixWord(1,text,column,shine)

    def deviceMatrixIcon(self,routeIcon,shine):
        matriz=[]
        #En la siguiente dirección se tendra que poner la ruta absoluta de los .txt que contiene las matrices booleanas
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

#----------------------------MP3---------------------------
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
        IDGround=["right","central","left"]  
        dicGround={}
        self.callback=True
        self.bot.requestLineFollower(3,"callbackGroundSensor")
        while self.callback:
            sleep(0.01)
        self.groundSensor=intAbin( self.groundSensor,3)
        print( self.groundSensor)
        for i,k in enumerate(IDGround):
            if self.groundSensor[i]=='1':
                dicGround[k]=0
            else:
                dicGround[k]=100
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

#---------------------------Controller---------------------------
    def callbackController(self,value):
        print("efectuando callback")
        self.controllerSensor=value
        self.callback=False

    def deviceReadControllerSensor(self):  
        IDButton=["rRight","rDown","rUp","rLeft","lDown","lRight","lLeft","lUp"]
        dicButton={}
        self.callback=True 
        self.bot.requestButton(4,"callbackController")
        while self.callback:
            sleep(0.01)    
        self.controllerSensor=intAbin( self.controllerSensor,8)
        print( self.controllerSensor)
        for i,k in enumerate(IDButton):
            if self.controllerSensor[i]=='1':
                dicButton[k]=True
            else:
                dicButton[k]=False
        print(dicButton)    
        return dicButton            

#Funcion de conversión de int a binario
def intAbin(val,bits):
    groundSensorBin=[]
    #Convertimos a binario 
    valBin=bin(val)
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


