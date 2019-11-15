# -*- coding: utf-8 -*-

try:
    from learnbot_dsl.Clients.Third_Party.VREP import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')
import sys
import numpy as np
from inputs import devices, get_gamepad
import time
from learnbot_dsl.Clients.Client import *
from learnbot_dsl.Clients.Devices import *
from learnbot_dsl.functions import getFuntions
import math, traceback, sys, tempfile, os
from threading import Event


__package__ = "EV3"

__version__ = "1.0.1"
__author__ = "Pablo Bustos"
__license__ = "GPL"

class VREPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_id = -1
        self.console_id = -1
        self.debug = False
        print("connecting to ", host, port)
        self.client_id = vrep.simxStart(self.host, 20000, True, True, 5000,5)
        print("connected!")
        if not self.is_connected():
            if self.debug:
                err_print(prefix="COMPONENT CREATION",
                          message=["CANNOT CONNECT TO REMOTE API"])
            raise Exception("CANNOT CONNECT TO REMOTE API")

    def is_debug_mode(self):
        return self.debug

    def set_debug(self, mode):
        self.debug = mode

    def is_connected(self):
        return self.client_id != -1       
        
    def init_terminal(self):
        err_list = []
        res, self.console_id = vrep.simxAuxiliaryConsoleOpen(
            self.client_id, "CONSOLA", 4, 5, None, None, None, None,
            vrep.simx_opmode_blocking)
        if res != 0:
            err_list = parse_error(res)
        return res, err_list

    def write_on_terminal(self, mess):
        res = vrep.simxAuxiliaryConsolePrint(self.client_id, self.console_id,
                                             mess, vrep.simx_opmode_blocking)
        return res, parse_error(res)

class Robot(Client):
    __COMPONENTS = {
        'robot': 'LEGO_EV3',
        'base':  'V_LEGO_EV3'
    }


    def __init__(self):
        Client.__init__(self, _miliseconds=100)
        self.connectToRobot()
        self.addBase(Base(_callFunction=self.deviceBaseMove))
        self.addGyroscope(Gyroscope(_readFunction=self.deviceReadGyroscope, _resetFunction=self.deviceResetGyroscope), "Z_AXIS")
        self.addDistanceSensors(DistanceSensors(_readFunction=self.deviceReadSonar))
        self.addGroundSensors(GroundSensors(_readFunction=self.deviceReadGroundSensors))
        self.start()

    def connectToRobot(self):
        host="127.0.0.1"
        port=20000
        suffix=""
        self.simEV3 = VREPClient(host, port)
        self.suffix = suffix
        self.components = {}
        self.handle_objects()
        self.objects = {}

    def disconnect(self):
        self.deviceBaseMove(0, 0)


    def handle_objects(self):
        for i, j in self.__COMPONENTS.items():
            self.components[i] = {'name': j + self.suffix, 'id': None}

        for i in self.components.keys():
            res, comp_id = vrep.simxGetObjectHandle(self.simEV3.client_id, self.components[i]['name'],vrep.simx_opmode_oneshot_wait)
            if res == 0:
                self.components[i]['id'] = comp_id
            elif res != 0 and self.debug:
                err_print(prefix="HANDLE OBJECTS:" +
                          self.components[i]['name'] + " ",
                          message=parse_error(res))

    def deviceBaseMove(self, SAdv, SRot):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.simEV3.client_id, "Funciones",  vrep.sim_scripttype_childscript, "On", [], [SAdv, math.radians(SRot)], [], emptyBuff, vrep.simx_opmode_blocking)		

    def deviceReadGyroscope(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.simEV3.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorGyroA", [], [], [], emptyBuff, vrep.simx_opmode_blocking)	
#        print("angle", outInts[0])
        if not outInts:
            return None
        else:
            return outInts[0]

    def deviceResetGyroscope(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.simEV3.client_id, "Funciones",  vrep.sim_scripttype_childscript, "ResetGyroA", [], [], [], emptyBuff, vrep.simx_opmode_blocking)		
        
    def deviceReadSonar(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.simEV3.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorSonar", [], [], [], emptyBuff, vrep.simx_opmode_blocking)	
        if not outFloats:
            return {}
        else:
            return {"front": [outFloats[0]*1000]}

    def deviceReadGroundSensors(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.simEV3.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorLight", [], [], [], emptyBuff, vrep.simx_opmode_blocking)		
        if not outInts:
            return {}
        else:
            return {"central": outInts[0]}



class EV3(VREPClient):

    __COMPONENTS = {
        'robot': 'LEGO_EV3',
        'base':  'V_LEGO_EV3'
    }

    def __init__(self, host="127.0.0.1", port=20000, suffix=""):
        VREPClient.__init__(self, host, port)
        self.suffix = suffix
        self.components = {}
        self.handle_objects()
        self.objects = {}
        #print(self.components)  #{'robot': {'name': 'Viriato', 'id': None}, 'base': {'name': 'viriato_base#', 'id': None}}

    def handle_objects(self):
        for i, j in EV3.__COMPONENTS.items():
            self.components[i] = {'name': j + self.suffix, 'id': None}

        for i in self.components.keys():
            res, comp_id = vrep.simxGetObjectHandle(self.client_id, self.components[i]['name'],vrep.simx_opmode_oneshot_wait)
            if res == 0:
                self.components[i]['id'] = comp_id
            elif res != 0 and self.debug:
                err_print(prefix="HANDLE OBJECTS:" +
                          self.components[i]['name'] + " ",
                          message=parse_error(res))

    def stop_base(self):
        err_list = []
                
    def set_base_speed(self, adv, rot):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "On", [], [adv, rot], [], emptyBuff, vrep.simx_opmode_blocking)		
        
    def get_sonar(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorSonar", [], [], [], emptyBuff, vrep.simx_opmode_blocking)		
        #res, sonar = vrep.simxGetObjectHandle(self.client_id, "mysonar", vrep.simx_opmode_oneshot_wait)
        #retCode, state, point, handle, normal = vrep.simxReadProximitySensor(self.client_id, sonar, vrep.simx_opmode_oneshot_wait)
        #print("sonar:", state, point)
        return outFloats

    def get_light_sensor(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorLight", [], [], [], emptyBuff, vrep.simx_opmode_blocking)		
        return outInts[0]

    def get_color_sensor(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorColor", [], [], [], emptyBuff, vrep.simx_opmode_blocking)
        return outFloats
    
    def get_angular_speed(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorGyroVA", [], [], [], emptyBuff, vrep.simx_opmode_blocking)		
        return outInts[0]

    def get_angle(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorGyroA", [], [], [], emptyBuff, vrep.simx_opmode_blocking)		
        return outInts[0]

    def get_base_pose(self):
        res, pos = vrep.simxGetObjectPosition(self.client_id, self.components['robot']['id'],-1, vrep.simx_opmode_blocking)
        if res != 0:
            err_print("GET BASE POSE", parse_error(res))
            raise Exception("ERROR IN GET BASE POSE")
        else:
            res, ang = vrep.simxGetObjectOrientation(self.client_id, self.components['robot']['id'], -1,vrep.simx_opmode_blocking)
            if res != 0:
                err_print("GET BASE POSE", parse_error(res))
                raise Exception("ERROR IN GET BASE POSE")
            else:
                ang = ang[1]
                return pos[0], pos[1], ang
        


if __name__ == "__main__":
    ev3 = EV3()
    #ev3.set_base_speed(0,0)
    adv = 0
    rot = 0
    MAX_ADV = 25 #mm/sg
    MAX_ROT = 1  #rads/sg
    start_time = time.time()
    while(True):
        elapsed_time = time.time() - start_time
        if elapsed_time > 0.5:
            print(ev3.get_base_pose())
            print("sonar:",ev3.get_sonar())
            print("image:",ev3.get_light_sensor())
            print("color:",ev3.get_color_sensor())
            print("angular speed:",ev3.get_angular_speed())
            print("angle:",ev3.get_angle())
            start_time = time.time()
        event = get_gamepad()[0]
        if event.code == "ABS_Y":
            adv = -event.state*MAX_ADV*2/256 + MAX_ADV
        elif event.code == "ABS_X":
            rot = -event.state*MAX_ROT*2/256 + MAX_ROT
        else:
            continue
        if abs(adv) > 0 or abs(rot) > 0:
            #print(event.code, event.state, adv,rot)
            ev3.set_base_speed(adv,rot)
        
            
        
            
