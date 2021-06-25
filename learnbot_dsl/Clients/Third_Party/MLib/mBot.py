# -*- coding: utf-8 -*

import serial
import sys,time
import signal
from time import ctime,sleep
import glob,struct
from multiprocessing import Process,Manager,Array
import threading

class mSerial():
    ser = None
    def __init__(self):
        sleep(0)

    def start(self, port):
        self.ser = serial.Serial(port,115200)
        #self.ser = serial.Serial(port,57600)
        #self.ser = serial.Serial(port,1200)
        print("is open", self.isOpen())
    
    def device(self):
        return self.ser

    def serialPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            s = serial.Serial()
            s.port = port
            s.close()
            result.append(port)
        return result

    def writePackage(self,package):
        print(package.hex())
        self.ser.write(package)
        sleep(0.01)

    def read(self):
        return self.ser.read()

    def isOpen(self):
        return self.ser.isOpen()

    def inWaiting(self):
        return self.ser.inWaiting()

    def close(self):
        self.ser.close()
        
class mBot():
    def __init__(self,obj):
        signal.signal(signal.SIGINT, self.exit)
        self.manager = Manager()
        self.__selectors = self.manager.dict()
        self.buffer = []
        self.bufferIndex = 0
        self.isParseStart = False
        self.exiting = False
        self.isParseStartIndex = 0
        self.obj=obj

        
    def startWithSerial(self, port):
        print("create serial")
        self.device = mSerial()
        self.device.start(port)
        self.start()
    
    def excepthook(self, exctype, value, traceback):
        print("Excepcion",exctype)
        print("Valor",value)
        print("traceback",traceback)
        self.close()
        
    def start(self):
        sys.excepthook = self.excepthook
        th = threading.Thread(target=self.__onRead,args=(self.onParse,))
        th.start()
        
    def close(self):
        self.device.close()
        
    def exit(self, signal, frame):
        self.exiting = True
        sys.exit(0)
        
    def __onRead(self,callback):
        while 1:
            if self.exiting:
                break
            if self.device.isOpen():
                n = self.device.inWaiting()
                for i in range(n):
                    r = ord(self.device.read())
                    callback(r)
                sleep(0.01)
            else:    
                sleep(0.5)
                
    def __writePackage(self,pack):
        self.device.writePackage(pack)

    ''''
    ESCRUCTURA COMANDO
    /**************************************************
      ff    55      len idx action device port slot data a
      0     1       2   3   4      5      6    7    8
    0xff  0x55   0x5 0x3 0x1    0x1    0x1  0xa 
      ***************************************************/
     '''

    '''
    Desc:Enviará el comando para encender los led de la placa
    Pre:0<port<5 && red,green y blue tienen que estar entre 0 y 254
    '''

    def doRGBLed(self,port,slot,index,red,green,blue):
        self.__writePackage(bytearray([0xff,0x55,0x9,0x0,0x2,0x8,self.limit(5,0,port),
                            self.limit(2,1,slot),self.limit(254,0,red),self.limit(254,0,green),self.limit(254,0,blue)]))

    '''
    Desc: Encenderá los led de la placa
    Pre:0<=red,green y blue<255
    '''
    def doRGBLedOnBoard(self,index,red,green,blue):
        self.doRGBLed(0x7,0x2,index,red,green,blue)

    '''
    Desc:Enviará el comando para encender uno de los motores, 
        port:Puerto seleccionado para elegir motor: izquierda es port=0 or 5, derecha port=6
    Pre:puerto=0 or 5 or 6 && 0<speed<255
    '''
    def doMotor(self,port,speed):
        b1 = bytearray([0xff,0x55,0x6,0x0,0x2,0xa,port])
        valSpeed=self.limit(32768,-32767,speed)
        b1.extend(valSpeed.to_bytes(2, 'little',signed=True))
        self.__writePackage(b1)

    '''
    Desc:Enviará el comando para encender los motores 
    Pre: 0<=leftSpeed<255 && 0<=speed<255
    '''
    def doMove(self,leftSpeed,rightSpeed):
        #self.__writePackage(bytearray([0xff,0x55,0x7,0x0,0x2,0x5]+self.short2bytes(-leftSpeed)+self.short2bytes(rightSpeed)))
        # self.__writePackage(bytearray([0xff,0x55,0x7,0x0,0x2,0x5]+(-leftSpeed).to_bytes(2, 'little')+rightSpeed.to_bytes(2,'little')))
        b1 = bytearray([0xff,0x55,0x7,0x0,0x2,0x5])
        valLeftSpeed=self.limit(32768,-32767,leftSpeed)
        valRightSpeed=self.limit(32768,-32767,rightSpeed)
        b1.extend(valLeftSpeed.to_bytes(2, 'little',signed=True))
        b1.extend(valRightSpeed.to_bytes(2, 'little',signed=True))
        self.__writePackage(b1)
        
    def doServo(self,port,slot,angle):
        self.__writePackage(bytearray([0xff,0x55,0x6,0x0,0x2,0xb,port,slot,angle]))
    
    '''
    Desc:
    '''
    def doBuzzer(self,buzzer,time=0):
        print("write")
        # self.__writePackage(bytearray([0xff,0x55,0x7,0x0,0x2,0x22]+self.short2bytes(buzzer)+self.short2bytes(time)))
        # self.__writePackage(bytearray([0xff,0x55,0x6,0x0,0x2,0x22, 0x9, 0x0, 0xa]))#+self.short2bytes(buzzer)+self.short2bytes(time)))
        b1 = bytearray([0xff,0x55,0x7,0x0,0x2,0x22])
        # print(self.short2bytes(buzzer))
        valBuzzer=self.limit(32768,-32767,buzzer)
        valTime=self.limit(32768,-32767,time)
        b1.extend(valBuzzer.to_bytes(2, 'little'))
        b1.extend(valTime.to_bytes(2, 'little'))
        self.__writePackage(b1)

    def doSevSegDisplay(self,port,display):
        self.__writePackage(bytearray([0xff,0x55,0x8,0x0,0x2,0x9,port]+self.float2bytes(display)))
        
    def doIROnBoard(self,message):
        self.__writePackage(bytearray([0xff,0x55,len(message)+3,0x0,0x2,0xd,message]))
    
    '''
    Desc:Enviará el comando para consultar el valor del luz de placa       
    '''  
    def requestLight(self,callback,extID=0):
        self.__doCallback(extID,callback)
        self.__writePackage(bytearray([0xff,0x55,0x4,extID,0x1,0x3,0x8]))

    def requestButtonOnBoard(self,callback,extID=1):
        self.__doCallback(extID,callback)
        self.__writePackage(bytearray([0xff,0x55,0x4,extID,0x1,0x1f,0x7]))
        
    '''
    Desc:Enviará el comando para consultar el valor del IR de placa       
    '''   
    def requestIROnBoard(self,callback,extID=2):
        self.__doCallback(extID,callback)
        self.__writePackage(bytearray([0xff,0x55,0x3,extID,0x1,0x12]))
    
    '''
    Desc:Enviará el comando para consultar la distancia del sensor de ultasonido
        port:Puerto conexionado en la placa mediante el rj12
    Pre:0<port<5      
    ''' 
    def requestUltrasonicSensor(self,port,callback,extID=3):
        self.__doCallback(extID,callback)
        self.__writePackage(bytearray([0xff,0x55,0x4,extID,0x1,0x1,self.limit(4,1,port)]))
        
    '''
    Desc:Enviará el comando para consultar el estado del siguelineas, 
        estará representadod por 3 bits en pormato decimal
        port:Puerto conexionado en la placa mediante el rj12
    Pre:0<port<5      
    '''
    def requestLineFollower(self,port,callback,extID=4):
        self.__doCallback(extID,callback)
        self.__writePackage(bytearray([0xff,0x55,0x4,extID,0x1,0x11,self.limit(4,1,port)]))
    
    def onParse(self, byte):
        position = 0
        value = 0    
        self.buffer+=[byte]
        bufferLength = len(self.buffer)
        if bufferLength >= 2:
            if (self.buffer[bufferLength-1]==0x55 and self.buffer[bufferLength-2]==0xff):
                self.isParseStart = True
                self.isParseStartIndex = bufferLength-2    
            if (self.buffer[bufferLength-1]==0xa and self.buffer[bufferLength-2]==0xd and self.isParseStart==True):            
                self.isParseStart = False
                position = self.isParseStartIndex+2
                extID = self.buffer[position]
                position+=1
                type = self.buffer[position]
                position+=1
                # 1 byte 2 float 3 short 4 len+string 5 double
                if type == 1:
                    value = self.buffer[position]
                if type == 2:
                    value = self.readFloat(position)
                    if(value<-255 or value>1023):
                        value = 0
                if type == 3:
                    value = self.readShort(position)
                if type == 4:
                    value = self.readString(position)
                if type == 5:
                    value = self.readDouble(position)
                if(type<=5):
                    self.responseValue(extID,value)
                self.buffer = []

    def readFloat(self, position):
        v = [self.buffer[position], self.buffer[position+1],self.buffer[position+2],self.buffer[position+3]]
        return struct.unpack('<f', struct.pack('4B', *v))[0]
    def readShort(self, position):
        v = [self.buffer[position], self.buffer[position+1]]
        return struct.unpack('<h', struct.pack('2B', *v))[0]
    def readString(self, position):
        l = self.buffer[position]
        position+=1
        s = ""
        for i in range(l):
            s += self.buffer[position+i].charAt(0)
        return s
    def readDouble(self, position):
        v = [self.buffer[position], self.buffer[position+1],self.buffer[position+2],self.buffer[position+3]]
        return struct.unpack('<f', struct.pack('4B', *v))[0]

    def responseValue(self, extID, value):
        #en el selector tenemos el nombre de la funcion, la buscamos en el objeto y la 
        #ejecutamos como callback
        fun=getattr(self.obj,self.__selectors["callback_"+str(extID)])       
        fun(value)  
        
    def __doCallback(self, extID, callback):
        self.__selectors["callback_"+str(extID)] = callback

    def float2bytes(self,fval):
        val = struct.pack("f",fval)
        return [ord(val[0]),ord(val[1]),ord(val[2]),ord(val[3])]

    def short2bytes(self,sval):
        print("sval.to_bytes()", sval.to_bytes(2, 'big'))
        return sval.to_bytes()
        # val = struct.pack("h",sval)
        #print("val", ord(val[0]))
        #return [ord(val[0]),ord(val[1])]

    def limit(self,max,min,val):
        if val>max:
            return max
        if val<min:
            return min
        return val