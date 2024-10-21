#!/usr/bin/env python
# -*- coding: utf-8 -*-
from learnbot_dsl.Clients.Client import *
from learnbot_dsl.Clients.Devices import *
import os, Ice, numpy as np, math
import learnbot_dsl.Clients.Devices as Devices
from learnbot_dsl import PATHINTERFACES

ROBOCOMP = ''
try:
    ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
    print('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
    ROBOCOMP = os.path.join('opt', 'robocomp')

ICEs = ["Laser.ice", "DifferentialRobot.ice"]
icePaths = []

icePaths.append(PATHINTERFACES)
for ice in ICEs:
    for p in icePaths:
        if os.path.isfile(os.path.join(p, ice)):
            wholeStr = ' -I' + p + " --all " + os.path.join(p, ice)
            Ice.loadSlice(wholeStr)
            break

import RoboCompLaser, RoboCompDifferentialRobot

class Robot(Client):
    def __init__(self):
        # Conectarse a los componentes de RoboComp
        self.connectToRobot()
        
        # Inicializar la clase padre
        Client.__init__(self)

        # Añadir los dispositivos necesarios: base y sensores de distancia (láser)
        self.addDistanceSensors(Devices.DistanceSensors(_readFunction=self.deviceReadLaser))
        self.addBase(Devices.Base(_callFunction=self.deviceMove))
        
        # Comenzar el loop de control
        self.start()

    def connectToRobot(self):
        # Conexión a differentialrobot en localhost:10004
        self.differentialrobot_proxy = connectComponent(
            "differentialrobot:tcp -p 10004", RoboCompDifferentialRobot.DifferentialRobotPrx)
        self.deviceMove(0, 0)  # Detener el robot al conectarse
        
        # Conexión a laser en localhost:10005
        self.laser_proxy = connectComponent(
            "laser:tcp -p 10005", RoboCompLaser.LaserPrx)

    def disconnect(self):
        # Parar el movimiento del robot al desconectar
        self.deviceMove(0, 0)

    def deviceReadLaser(self):
        # Leer datos del LIDAR a través del proxy de laser
        laserdata = self.laser_proxy.getLaserData()
        usList = [d.dist for d in laserdata]  # Extraer las distancias
        # Retornar datos en mm para los lados "frontal", "izquierda", "derecha"
        return {
            "front": usList[1:4],  # Selecciona las lecturas frontales
            "left": usList[:2],    # Selecciona las lecturas a la izquierda
            "right": usList[4:]    # Selecciona las lecturas a la derecha
        }

    def deviceMove(self, _adv, _rot):
        # Controlar la base del robot (avanzar y rotar)
        self.differentialrobot_proxy.setSpeedBase(_adv, math.radians(_rot))

if __name__ == '__main__':
    robot = Robot()
    
    print(robot.__dict__)  # Mostrar los atributos del robot para depuración
    
    robot.deviceMove(10, 10)
